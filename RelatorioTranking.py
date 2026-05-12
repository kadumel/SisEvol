"""
Relatório de tracking de preços: consulta VW_TRACKING, monta HTML (modelo e-mail)
e envia via SMTP. Os valores exibidos vêm da view já formatados.

Uso (na pasta SisEvol, com venv ativo):
    python RelatorioTranking.py
    python RelatorioTranking.py --to destino@empresa.com
    python RelatorioTranking.py --per-empresa

Agendamento com Django-Q2 (``python manage.py qcluster``):
    Função: ``RH.tasks_tracking.enviar_relatorio_tracking_precos`` (ver docstring nesse módulo).
    Chama ``run_relatorio_tracking_job()`` — mesma lógica que a CLI, sem ``--show-columns``.

Variáveis de ambiente úteis (.env):
    TRACKING_EMAIL_TO          destinatário(s) fixos (opcional): sobrescreve e-mails de EmailRelatorio
    TRACKING_EMAIL_SUBJECT   assunto (padrão: Relatório — Tracking de preços)
    VW_TRACKING_NAME         nome da view (padrão: VW_TRACKING)
    TRACKING_MAP_ID          nome exato da coluna (view) para ID ERP
    TRACKING_MAP_DESC        coluna descrição / produto
    TRACKING_MAP_ONTEM      coluna preço ontem
    TRACKING_MAP_HOJE       coluna preço hoje
    TRACKING_MAP_VAR        coluna variação (%)
    TRACKING_MAP_TIPO       coluna que define aumento vs redução (obrigatória para classificar)
    TRACKING_MAP_RN         coluna ranking na view (padrão: detecta `rn` ou nomes parecidos)
    TRACKING_MAP_DATA_COMPRA / TRACKING_MAP_DATA  coluna de data do registro ou da última compra
      (opcional). Se existir, o e-mail mostra o MAX dessa data por empresa acima das tabelas.

    Alternativa (mesmo efeito; primeira variável encontrada no .env ganha):
    ID_ERP, DESCRICAO, ONTEM, HOJE, VARIACAO, TIPO, RANKING
    (e opcionalmente DATA_COMPRA / TRACKING_MAP_DATA_COMPRA para a data do último registro)

    Um único e-mail (TRACKING_PER_EMPRESA=false): destinatários vêm de RH.EmailRelatorio
    (relatorio_tracking='S') para cada empresa que aparecer na view — mapeie a coluna
    EMPRESA / TRACKING_MAP_EMPRESA. TRACKING_EMAIL_TO ou --to sobrescrevem a lista.

    Um e-mail por empresa (TRACKING_PER_EMPRESA=true):
    — Coluna de agrupamento: TRACKING_MAP_EMPRESA ou EMPRESA, CD_EMPRESA, etc.
    — Destinatários: TRACKING_EMPRESA_EMAIL_SOURCE=django (padrão) usa RH.EmailRelatorio
      (empresa + relatorio_tracking='S' + e-mail).
    — Ou TRACKING_EMPRESA_EMAIL_SOURCE=env e TRACKING_EMAIL_MAP=12=a@x.com;34=b@y.com

As colunas são lidas da view (metadados + heurística). Use --show-columns para
conferir o mapeamento ou as variáveis TRACKING_MAP_* para forçar nomes exatos.
A coluna tipo é a única usada para separar aumentos e reduções (não se usa o sinal da variação).
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
import unicodedata
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# Garantir que o pacote Django encontre o projeto
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

load_dotenv(BASE_DIR / ".env")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django

django.setup()

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import connection


VIEW_NAME = os.getenv("VW_TRACKING_NAME", "VW_TRACKING")

# Pontuação mínima para aceitar mapeamento automático por papel
_MIN_AUTO_SCORE = 4


def _validate_view_sql_fragment(view: str) -> None:
    view = view.strip()
    if not re.fullmatch(r"[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)?", view):
        raise ValueError(
            "Nome de view inválido. Use apenas letras, números, _ e opcionalmente schema "
            "(ex.: VW_TRACKING ou dbo.VW_TRACKING)."
        )


def split_view_schema_name(view: str) -> tuple[str, str]:
    view = view.strip()
    _validate_view_sql_fragment(view)
    if "." in view:
        schema, name = view.split(".", 1)
        return schema.strip(), name.strip()
    return "dbo", view


def fetch_view_column_names(view: str) -> list[str]:
    """
    Colunas expostas pela view, na ordem do resultado — via SELECT TOP 0 *
    (mesmos identificadores que SELECT *). Se falhar, tenta INFORMATION_SCHEMA.
    """
    _validate_view_sql_fragment(view)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT TOP 0 * FROM {view}")
        desc = cursor.description
        if desc:
            return [d[0] for d in desc]
    schema, table = split_view_schema_name(view)
    cols: list[str] = []
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE UPPER(TABLE_SCHEMA) = UPPER(%s) AND UPPER(TABLE_NAME) = UPPER(%s)
            ORDER BY ORDINAL_POSITION
            """,
            [schema, table],
        )
        cols = [row[0] for row in cursor.fetchall()]
    if not cols:
        raise RuntimeError(
            f"Não foi possível obter colunas da view {view!r}. "
            "Verifique o nome (schema.view) e permissões."
        )
    return cols


def _fold_name(name: str) -> str:
    """ASCII upper + underscores para comparar nomes de coluna."""
    s = unicodedata.normalize("NFKD", name or "")
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", "_", s.strip()).upper()


def _normalize_env_value(raw: str) -> str:
    """Remove aspas externas e espaços (ex.: 'cdEmpresa' -> cdEmpresa)."""
    s = str(raw).strip()
    if len(s) >= 2 and s[0] in "'\"" and s[-1] == s[0]:
        s = s[1:-1].strip()
    return s


def _find_col_by_wanted_name(wanted: str, colnames: list[str]) -> str | None:
    """Resolve o nome físico da coluna na view (case / acentos)."""
    idx = {c.upper(): c for c in colnames}
    if wanted.upper() in idx:
        return idx[wanted.upper()]
    fold_idx = {_fold_name(c): c for c in colnames}
    fk = _fold_name(wanted)
    if fk in fold_idx:
        return fold_idx[fk]
    return None


def _resolve_env_column_chain(colnames: list[str], *env_keys: str) -> str | None:
    """
    Usa a primeira variável de ambiente definida (não vazia), nesta ordem.
    TRACKING_MAP_* tem prioridade sobre os nomes curtos (ID_ERP, DESCRICAO, ...).
    """
    for env_key in env_keys:
        raw = os.getenv(env_key)
        if raw is None or not str(raw).strip():
            continue
        wanted = _normalize_env_value(raw)
        if not wanted:
            continue
        hit = _find_col_by_wanted_name(wanted, colnames)
        if hit:
            return hit
        raise RuntimeError(
            f"{env_key}={raw!r} (coluna {wanted!r}) não corresponde a nenhuma coluna da view. "
            f"Colunas: {', '.join(colnames)}"
        )
    return None


def _score_role(folded: str, role: str) -> int:
    """Pontua heurística: quanto maior, melhor o match do papel."""
    n = folded
    if role == "rn":
        if n == "RN":
            return 20
        if re.search(r"^RN(_|$)", n) or re.search(r"_RN$", n):
            return 16
        if re.search(r"RANK(ING)?|ROW_NUMBER|ROWNUM|POSI(C|Ç)AO|POSIÇÃO|ORDEM_RANK", n):
            return 12
        return 0
    if role == "var":
        s = 0
        if re.search(r"VARIAC|VAR_PCT|PCT_VAR|PERCENT|PERC(ENT)?", n):
            s += 14
        if "%" in n or "PCT" in n or "PERC" in n:
            s += 6
        if "DELTA" in n or "VAR_" in n or n.endswith("_VAR"):
            s += 8
        if s and "PRECO" in n and "VAR" not in n:
            s -= 3
        return s
    if role == "ontem":
        s = 0
        if "ONTEM" in n or "YESTERDAY" in n or "ANTERIOR" in n or "DIA_ANT" in n:
            s += 14
        if "PREV" in n or "_D1" in n or n.endswith("_1"):
            s += 6
        if "PRECO" in n and ("ONT" in n or "ANT" in n):
            s += 10
        if "VL_" in n and "ONT" in n:
            s += 10
        if n == "ONTEM":
            s += 12
        return s
    if role == "hoje":
        s = 0
        if "HOJE" in n or "TODAY" in n or "ATUAL" in n or "CURRENT" in n:
            s += 14
        if "PRECO" in n and ("HOJE" in n or "ATU" in n):
            s += 10
        if "VL_" in n and "HOJE" in n:
            s += 10
        if n == "HOJE":
            s += 12
        return s
    if role == "id":
        s = 0
        if re.search(r"(ID|COD).*ERP|ERP.*(ID|COD)", n):
            s += 16
        if re.search(r"^COD(IGO)?(_|.)?(ERP|PROD|ITEM)", n):
            s += 15
        if "SKU" in n:
            s += 10
        if re.search(r"^ID(_PRODUTO|PRODUTO|_PROD)?$", n):
            s += 8
        if "ID" in n and ("PROD" in n or "ITEM" in n):
            s += 9
        if n in ("ID", "ID_ERP", "COD_ERP", "CODIGO_ERP"):
            s += 7
        return s
    if role == "desc":
        s = 0
        if "DESCR" in n or "DENOMIN" in n:
            s += 14
        if "NOME" in n and "PROD" in n:
            s += 12
        if n in ("PRODUTO", "ITEM", "NOME", "NM_PRODUTO", "NOME_PRODUTO"):
            s += 10
        if "PROD" in n and "ID" not in n and "COD" not in n:
            s += 5
        return s
    if role == "tipo":
        s = 0
        if re.search(r"TIPO|MOVIMENT|DIREC|SINAL|SECAO|SECÇ", n):
            s += 12
        if n in ("AUMENTO", "REDUCAO", "SENTIDO"):
            s += 8
        return s
    if role == "empresa":
        s = 0
        if re.search(r"CD_?EMPRESA|COD_?EMPRESA|EMPRESA_?ID|ID_?EMPRESA|CODIGO_?EMPRESA", n):
            s += 16
        if "EMPRESA" in n and "PROD" not in n and "PRODUTO" not in n and "NM" not in n:
            s += 10
        if re.search(r"FILIAL|UNIDADE|COD_?BI|CODIGO_?BI|EMPRESA_?RAIZ", n):
            s += 8
        if n == "EMPRESA":
            s += 6
        return s
    if role == "data_reg":
        if "NASC" in n or "NASCIMENTO" in n:
            return 0
        s = 0
        if re.search(r"DATA.*COMPRA|COMPRA|DT.*COMPRA|ULTIMA.*COMPRA|ULT_COMPRA|ULT_COMPR", n):
            s += 18
        if re.search(r"DATA.*MOV|DT_MOV|DATA_MOV|DATA_REG|DT_REG|REFEREN|DT_ULT", n):
            s += 14
        if re.search(r"EMISS|FATURA|LANC|LANÇ", n):
            s += 6
        if n in ("DATA", "DT") or n.startswith("DT_") or n.startswith("DATA_"):
            s += 8
        return s
    return 0


def infer_column_mapping(colnames: list[str]) -> dict[str, str | None]:
    """
    Mapeia papéis lógicos -> nome real da coluna.
    Papéis: id, desc, ontem, hoje, var, tipo, rn, data_reg, empresa (empresa = agrupamento / código BI).
    data_reg = data do registro / última compra (opcional, para texto no e-mail).
    """
    if not colnames:
        raise RuntimeError("A view não retornou nomes de coluna.")

    # Sobrescritas via .env: TRACKING_MAP_* ou nomes alternativos (ID_ERP, DESCRICAO, ...)
    out: dict[str, str | None] = {
        "id": _resolve_env_column_chain(colnames, "TRACKING_MAP_ID", "ID_ERP"),
        "desc": _resolve_env_column_chain(
            colnames, "TRACKING_MAP_DESC", "DESCRICAO", "DESCRIÇÃO"
        ),
        "ontem": _resolve_env_column_chain(colnames, "TRACKING_MAP_ONTEM", "ONTEM"),
        "hoje": _resolve_env_column_chain(colnames, "TRACKING_MAP_HOJE", "HOJE"),
        "var": _resolve_env_column_chain(
            colnames, "TRACKING_MAP_VAR", "VARIACAO", "VARIAÇÃO"
        ),
        "tipo": _resolve_env_column_chain(colnames, "TRACKING_MAP_TIPO", "TIPO"),
        "rn": _resolve_env_column_chain(colnames, "TRACKING_MAP_RN", "RANKING"),
        "data_reg": _resolve_env_column_chain(
            colnames,
            "TRACKING_MAP_DATA_COMPRA",
            "TRACKING_MAP_DATA",
            "DATA_COMPRA",
            "DT_COMPRA",
            "DT_ULTIMA_COMPRA",
            "DATA_ULTIMA_COMPRA",
            "DATA_REGISTRO",
            "DT_REGISTRO",
        ),
        "empresa": _resolve_env_column_chain(
            colnames,
            "TRACKING_MAP_EMPRESA",
            "EMPRESA",
            "CD_EMPRESA",
            "COD_EMPRESA",
            "CODIGO_EMPRESA",
            "EMPRESA_ID",
        ),
    }

    folded = {c: _fold_name(c) for c in colnames}
    used: set[str] = {v for v in out.values() if v}

    # Tipo, ranking, demais; data_reg antes de empresa; empresa por último
    role_order = ("tipo", "rn", "var", "ontem", "hoje", "id", "desc", "data_reg", "empresa")

    for role in role_order:
        if out[role]:
            continue
        best_col: str | None = None
        best_score = 0
        for c in colnames:
            if c in used:
                continue
            sc = _score_role(folded[c], role)
            if sc > best_score:
                best_score = sc
                best_col = c
        if role == "tipo":
            out[role] = best_col if best_score >= _MIN_AUTO_SCORE else None
            if out[role]:
                used.add(out[role])
            continue
        if role == "data_reg":
            min_score = 6
            out[role] = best_col if best_col and best_score >= min_score else None
            if out[role]:
                used.add(out[role])
            continue
        if best_col is None or best_score < _MIN_AUTO_SCORE:
            out[role] = None
        else:
            out[role] = best_col
            used.add(best_col)

    return out


def align_mapping_to_cursor_keys(
    mapping: dict[str, str | None], colnames_exec: list[str]
) -> dict[str, str | None]:
    """Garante que os nomes no mapeamento coincidam com os de cursor.description (casing)."""
    by_upper = {c.upper(): c for c in colnames_exec}
    out: dict[str, str | None] = {}
    for k, v in mapping.items():
        if not v:
            out[k] = None
            continue
        out[k] = by_upper.get(v.upper(), v if v in colnames_exec else None)
    return out


def format_mapping_report(colnames: list[str], mapping: dict[str, str | None]) -> str:
    lines = [
        f"View: {VIEW_NAME}",
        f"Colunas ({len(colnames)}): " + ", ".join(colnames),
        "Mapeamento para o relatório:",
    ]
    labels = [
        ("id", "ID ERP"),
        ("desc", "Descrição"),
        ("ontem", "Ontem"),
        ("hoje", "Hoje"),
        ("var", "Variação"),
        ("tipo", "Tipo (aumento / redução)"),
        ("rn", "Ranking (rn)"),
        ("data_reg", "Data registro / última compra (opcional)"),
        ("empresa", "Empresa (agrupamento)"),
    ]
    for key, label in labels:
        v = mapping.get(key)
        lines.append(f"  {label}: {v!r}" if v else f"  {label}: (não mapeado)")
    return "\n".join(lines)


def _tipo_is_reducao(raw) -> bool | None:
    """
    Interpreta o valor da coluna tipo da view.
    True = redução, False = aumento, None = valor não reconhecido.
    """
    if raw is None:
        return None
    if isinstance(raw, str) and not raw.strip():
        return None
    # BIT / tinyint numérico vindo do driver
    if isinstance(raw, bool):
        return None
    s = str(raw).strip().upper()
    # Também compara versão sem acentos (ex.: view devolve "Diminuição")
    s_fold = _fold_name(str(raw).strip())
    reducao = {
        "R",
        "REDUCAO",
        "REDUÇÃO",
        "REDUÇAO",
        "D",
        "DOWN",
        "DECREASE",
        "MENOR",
        "-",
        "RED",
        "NEG",
        "NEGATIVO",
        "QUEDA",
        "0",
        "DIMINUIÇÃO",
        "DIMINUICAO",
        "BAIXA",
        "MENOS",
        "DESCIDA",
    }
    aumento = {
        "A",
        "AUMENTO",
        "UP",
        "INCREASE",
        "MAIOR",
        "+",
        "INC",
        "POS",
        "POSITIVO",
        "SOBE",
        "1",
        "ELEVAÇÃO",
        "ELEVACAO",
        "ALTA",
        "CRESCIMENTO",
        "SUBIDA",
        "CRESCEU",
    }
    if s in reducao or s_fold in reducao:
        return True
    if s in aumento or s_fold in aumento:
        return False
    try:
        n = float(str(raw).replace(",", "."))
        if n < 0:
            return True
        if n > 0:
            return False
    except ValueError:
        pass
    return None


def _sort_key_by_rn(row: dict) -> tuple:
    """Ordena pelo ranking numérico da coluna rn quando existir."""
    if "rn" not in row:
        return (0, 0.0)
    v = row["rn"]
    if v is None:
        return (1, 0.0)
    try:
        return (0, float(str(v).replace(",", ".").replace(" ", "")))
    except ValueError:
        return (2, str(v))


def _env_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None or not str(v).strip():
        return default
    return str(v).strip().lower() in ("1", "true", "yes", "sim", "on")


def _empresa_key_for_row(emp_raw) -> str:
    if emp_raw is None:
        return ""
    if isinstance(emp_raw, bool):
        return str(int(emp_raw))
    if isinstance(emp_raw, float):
        if emp_raw.is_integer():
            return str(int(emp_raw))
        return str(emp_raw).strip()
    if isinstance(emp_raw, int):
        return str(int(emp_raw))
    return str(emp_raw).strip()


def _norm_map_key_for_empresa(emp_key: str) -> str:
    s = emp_key.strip()
    try:
        f = float(s)
        if f == int(f):
            return str(int(f))
    except ValueError:
        pass
    return s


def _parse_tracking_email_map() -> dict[str, list[str]]:
    raw = os.getenv("TRACKING_EMAIL_MAP", "")
    out: dict[str, list[str]] = {}
    if not raw or not str(raw).strip():
        return out
    for part in str(raw).split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        lhs, rhs = part.split("=", 1)
        key_norm = _norm_map_key_for_empresa(str(lhs).strip())
        emails = [e.strip() for e in re.split(r"[,;]", rhs) if e.strip()]
        if key_norm and emails:
            out[key_norm] = emails
    return out


def _django_empresa_nome(codigo_bi: int) -> str | None:
    try:
        from RH.models import Empresa
    except ImportError:
        return None
    e = Empresa.objects.filter(codigo_BI=codigo_bi).first()
    return e.empresa if e else None


def _recipient_emails_for_empresa(emp_key: str) -> list[str]:
    source = (os.getenv("TRACKING_EMPRESA_EMAIL_SOURCE") or "django").strip().lower()
    if source == "env":
        m = _parse_tracking_email_map()
        if not m:
            return []
        nk = _norm_map_key_for_empresa(emp_key)
        if nk in m:
            return m[nk]
        sk = emp_key.strip()
        if sk in m:
            return m[sk]
        return []

    try:
        from RH.models import Empresa, EmailRelatorio
    except ImportError:
        return []

    emp = None
    nk = _norm_map_key_for_empresa(emp_key)
    if nk.lstrip("-").isdigit():
        try:
            cbi = int(float(nk))
            emp = Empresa.objects.filter(codigo_BI=cbi).first()
        except ValueError:
            emp = None
    if emp is None and emp_key.strip():
        emp = Empresa.objects.filter(empresa__iexact=emp_key.strip()).first()
    if not emp:
        return []

    emails: list[str] = []
    qs = EmailRelatorio.objects.filter(
        empresa=emp,
        relatorio_tracking="S",
    ).exclude(email_empresa__isnull=True).exclude(email_empresa="")
    for raw in qs.values_list("email_empresa", flat=True).distinct():
        for e in re.split(r"[\s;,]+", str(raw).strip()):
            if e:
                emails.append(e)
    return list(dict.fromkeys(emails))


def _recipients_for_empresa_keys_aggregate(emp_keys: frozenset[str] | set[str]) -> list[str]:
    """Junta e-mails de EmailRelatorio (ou mapa .env) para todas as chaves de empresa do relatório."""
    acc: list[str] = []
    for ek in emp_keys:
        if not ek or ek == "__sem_empresa__":
            continue
        acc.extend(_recipient_emails_for_empresa(ek))
    return list(dict.fromkeys(acc))


def _bundle_empresa_label(emp_key: str) -> str:
    if emp_key == "__sem_empresa__":
        return "(sem empresa)"
    nk = _norm_map_key_for_empresa(emp_key)
    if nk.lstrip("-").isdigit():
        try:
            cbi = int(float(nk))
            nome = _django_empresa_nome(cbi)
            if nome:
                return f"{nome} (BI {cbi})"
        except ValueError:
            pass
    return emp_key


def _format_date_br(d: date | datetime) -> str:
    if isinstance(d, datetime):
        d = d.date()
    return d.strftime("%d/%m/%Y")


def _parse_row_date(val) -> date | None:
    """Normaliza valor da view (date/datetime/string) para date, ou None."""
    if val is None:
        return None
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, date):
        return val
    s = str(val).strip()
    if not s:
        return None
    if len(s) >= 10 and s[4] == "-" and s[7] == "-":
        try:
            return date.fromisoformat(s[:10])
        except ValueError:
            pass
    for fmt in (
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(s[:26].strip(), fmt).date()
        except ValueError:
            continue
    return None


def build_ultima_registro_html(max_by_emp: dict[str, date]) -> str | None:
    """
    HTML do bloco “último registro / última compra” para o e-mail agregado (várias empresas).
    Chaves: código/nome de empresa ou '__global__' quando não há coluna empresa.
    """
    if not max_by_emp:
        return None
    items = [(k, v) for k, v in max_by_emp.items() if v is not None]
    if not items:
        return None
    p_style = (
        "font-family:Arial,sans-serif;font-size:13px;color:#444;margin:0 0 18px 0;"
    )

    if len(items) == 1:
        ek, d = items[0]
        if ek == "__global__":
            inner = (
                "Data do último registro na base (última compra): "
                f"<strong>{html.escape(_format_date_br(d), quote=True)}</strong>."
            )
        else:
            lbl = _bundle_empresa_label(ek)
            inner = (
                f"Último registro para <strong>{html.escape(lbl, quote=True)}</strong> "
                f"(data da última compra): <strong>{html.escape(_format_date_br(d), quote=True)}</strong>."
            )
        return f'<p style="{p_style}">{inner}</p>'

    non_global = [(k, v) for k, v in items if k != "__global__"]
    if not non_global:
        return None
    li_parts = []
    for ek, d in sorted(non_global, key=lambda x: _bundle_empresa_label(x[0]).lower()):
        lbl = _bundle_empresa_label(ek)
        li_parts.append(
            f'<li style="margin:4px 0;"><strong>{html.escape(lbl, quote=True)}</strong>: '
            f"{html.escape(_format_date_br(d), quote=True)}</li>"
        )
    intro = "Data do último registro na base por empresa (última compra conhecida):"
    return (
        f'<div style="{p_style}">'
        f'<p style="margin:0 0 8px 0;">{html.escape(intro)}</p>'
        f'<ul style="margin:0;padding-left:20px;">{"".join(li_parts)}</ul>'
        "</div>"
    )


def _ultima_registro_html_single(dt: date | None) -> str | None:
    """Um parágrafo: data máxima já filtrada para a empresa do e-mail."""
    if not dt:
        return None
    p_style = (
        "font-family:Arial,sans-serif;font-size:13px;color:#444;margin:0 0 18px 0;"
    )
    s = _format_date_br(dt)
    inner = (
        "Data do último registro na base (última compra): "
        f"<strong>{html.escape(s, quote=True)}</strong>."
    )
    return f'<p style="{p_style}">{inner}</p>'


def fetch_tracking_rows(
    per_empresa: bool = False,
) -> (
    tuple[list[dict], list[dict], frozenset[str], str | None]
    | dict[str, dict[str, Any]]
):
    """
    Lê colunas da view, infere mapeamento, executa SELECT *.
    Se per_empresa=True, devolve dict[empresa_key, {"aumentos","reducoes","label","ultima_data"}].
    Caso contrário, (aumentos, reduções, chaves_empresa_distintas, html_ultimo_registro | None)
    para destinatários em EmailRelatorio quando existir coluna empresa mapeada na view.
    """
    view = VIEW_NAME.strip()
    colnames = fetch_view_column_names(view)
    mapping = infer_column_mapping(colnames)
    mapping = align_mapping_to_cursor_keys(mapping, colnames)

    required = ("id", "desc", "ontem", "hoje", "var", "tipo")
    if per_empresa:
        required = (*required, "empresa")
    missing = [r for r in required if not mapping.get(r)]
    if missing:
        raise RuntimeError(
            "Não foi possível mapear automaticamente: "
            + ", ".join(missing)
            + ".\n"
            + format_mapping_report(colnames, mapping)
            + "\nDefina TRACKING_MAP_* / ID_ERP / EMPRESA= no .env conforme a view."
        )

    sql = f"SELECT * FROM {view}"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        desc = cursor.description
        if not desc:
            if per_empresa:
                return {}
            return [], [], frozenset(), None
        colnames_exec = [d[0] for d in desc]
        mapping_exec = align_mapping_to_cursor_keys(mapping, colnames_exec)

        missing_exec = [r for r in required if not mapping_exec.get(r)]
        if missing_exec:
            raise RuntimeError(
                "Colunas mapeadas não aparecem no SELECT * da view: "
                + ", ".join(missing_exec)
                + ".\n"
                + format_mapping_report(colnames_exec, mapping_exec)
            )

        col_id = mapping_exec["id"]
        col_desc = mapping_exec["desc"]
        col_ontem = mapping_exec["ontem"]
        col_hoje = mapping_exec["hoje"]
        col_var = mapping_exec["var"]
        col_tipo = mapping_exec["tipo"]
        col_rn = mapping_exec.get("rn")
        col_empresa = mapping_exec.get("empresa")
        col_data = mapping_exec.get("data_reg")
        empresa_keys_found: set[str] = set()
        max_date_by_emp: dict[str, date] = {}

        if per_empresa and not col_empresa:
            raise RuntimeError(
                "TRACKING_PER_EMPRESA exige coluna de empresa na view. "
                "Defina EMPRESA= ou TRACKING_MAP_EMPRESA= com o nome da coluna (ex.: codigo_BI da filial)."
            )

        aumentos: list[dict] = []
        reducoes: list[dict] = []
        buckets: dict[str, dict[str, Any]] = {}

        for row in cursor.fetchall():
            d = dict(zip(colnames_exec, row))

            if col_data:
                dt = _parse_row_date(d.get(col_data))
                if dt:
                    if col_empresa:
                        ekd = _empresa_key_for_row(d.get(col_empresa))
                        if not ekd:
                            ekd = "__sem_empresa__"
                    else:
                        ekd = "__global__"
                    old = max_date_by_emp.get(ekd)
                    if old is None or dt > old:
                        max_date_by_emp[ekd] = dt

            tipo_raw = d.get(col_tipo)
            tr = _tipo_is_reducao(tipo_raw)
            if tr is None:
                raise RuntimeError(
                    "A coluna tipo define aumento ou redução; o valor desta linha não foi "
                    f"reconhecido. Coluna {col_tipo!r}, valor {tipo_raw!r}, "
                    f"ID ERP={d.get(col_id)!r}. "
                    "Amplie _tipo_is_reducao em RelatorioTranking.py ou ajuste a view."
                )

            entry = {
                "id": d[col_id],
                "desc": d[col_desc],
                "ontem": _format_two_decimals_cell(d[col_ontem]),
                "hoje": _format_two_decimals_cell(d[col_hoje]),
                "var": _format_two_decimals_cell(d[col_var], suffix_percent=True),
            }
            if col_rn:
                entry["rn"] = d[col_rn]

            if per_empresa:
                ek = _empresa_key_for_row(d.get(col_empresa))
                if not ek:
                    ek = "__sem_empresa__"
                if ek not in buckets:
                    buckets[ek] = {
                        "aumentos": [],
                        "reducoes": [],
                        "label": _bundle_empresa_label(ek),
                    }
                if tr:
                    buckets[ek]["reducoes"].append(entry)
                else:
                    buckets[ek]["aumentos"].append(entry)
            else:
                if col_empresa:
                    ek = _empresa_key_for_row(d.get(col_empresa))
                    if ek:
                        empresa_keys_found.add(ek)
                if tr:
                    reducoes.append(entry)
                else:
                    aumentos.append(entry)

        if per_empresa:
            for b in buckets.values():
                au, rd = b["aumentos"], b["reducoes"]
                if au and "rn" in au[0]:
                    au.sort(key=_sort_key_by_rn)
                if rd and "rn" in rd[0]:
                    rd.sort(key=_sort_key_by_rn)
            for ek, b in buckets.items():
                b["ultima_data"] = max_date_by_emp.get(ek)
            return buckets

        if aumentos and "rn" in aumentos[0]:
            aumentos.sort(key=_sort_key_by_rn)
        if reducoes and "rn" in reducoes[0]:
            reducoes.sort(key=_sort_key_by_rn)

        ultima_html = (
            build_ultima_registro_html(max_date_by_emp) if col_data else None
        )

        return aumentos, reducoes, frozenset(empresa_keys_found), ultima_html


def _parse_numeric_for_display(val) -> float | None:
    """Extrai número para arredondar (aceita BR, R$, %, Decimal)."""
    if val is None:
        return None
    if isinstance(val, bool):
        return None
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip()
    if not s:
        return None
    s = s.replace("−", "-")
    s = re.sub(r"(?i)R\$\s*", "", s)
    s = re.sub(r"\s*%$", "", s).strip()
    s = re.sub(r"(\d)\s+(?=\d)", r"\1", s)
    sign = 1
    if s.startswith("-"):
        sign = -1
        s = s[1:].strip()
    elif s.startswith("+"):
        s = s[1:].strip()
    if not s:
        return None
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return sign * float(s)
    except ValueError:
        return None


def _format_two_decimals_cell(val, suffix_percent: bool = False) -> str:
    """
    Ontem / hoje / variação com duas casas decimais (vírgula decimal, estilo BR).
    Preserva R$ quando já existia no valor original.
    Se suffix_percent=True (coluna variação), o resultado termina sempre com %.
    """
    if val is None:
        return ""
    s_orig = str(val).strip()
    if not s_orig:
        return ""

    n = _parse_numeric_for_display(val)
    if n is None:
        return s_orig

    body = f"{abs(n):.2f}".replace(".", ",")
    upper = s_orig.upper()
    has_rs = "R$" in upper
    has_pct = "%" in s_orig

    if has_rs:
        return f"R$ {body}" if n >= 0 else f"-R$ {body}"
    if suffix_percent or has_pct:
        if n < 0:
            return f"-{body}%"
        if n > 0:
            return f"+{body}%"
        return f"{body}%"
    if s_orig.strip().startswith(("-", "−")):
        return f"-{body}"
    if s_orig.strip().startswith("+"):
        return f"+{body}"
    return body if n >= 0 else f"-{body}"


def _cell_txt(v) -> str:
    if v is None:
        return ""
    return html.escape(str(v), quote=True)


def _build_table(
    title: str,
    title_bg: str,
    header_row_bg: str,
    rows: list[dict],
    var_positive: bool,
    show_ranking: bool,
) -> str:
    """
    var_positive: True = aumentos (variação em vermelho); False = reduções (variação em azul).
    show_ranking: primeira coluna com o valor da coluna rn (ranking) da view.
    """
    var_color = "#C62828" if var_positive else "#1565C0"
    icon = "&#9650;" if var_positive else "&#9660;"
    ncol = 5 if show_ranking else 4

    if not rows:
        body = (
            f'<tr><td colspan="{ncol}" style="padding:12px;font-family:Arial,sans-serif;'
            f'font-size:13px;color:#555;">Nenhum registro.</td></tr>'
        )
    else:
        parts = []
        for i, r in enumerate(rows):
            bg = "#FFFFFF" if i % 2 == 0 else "#F5F9FC"
            rank_cell = ""
            if show_ranking:
                rank_cell = (
                    f'<td style="padding:8px 10px;font-family:Arial,sans-serif;font-size:13px;'
                    f'text-align:right;border-bottom:1px solid #E0E0E0;background-color:{bg};">'
                    f"{_cell_txt(r.get('rn'))}</td>"
                )
            parts.append(
                "<tr>"
                f"{rank_cell}"
                f'<td style="padding:8px 10px;font-family:Arial,sans-serif;font-size:13px;'
                f'text-align:left;border-bottom:1px solid #E0E0E0;background-color:{bg};">'
                f"{_cell_txt(r['desc'])}</td>"
                f'<td style="padding:8px 10px;font-family:Arial,sans-serif;font-size:13px;'
                f'text-align:right;border-bottom:1px solid #E0E0E0;background-color:{bg};">'
                f"{_cell_txt(r['ontem'])}</td>"
                f'<td style="padding:8px 10px;font-family:Arial,sans-serif;font-size:13px;'
                f'text-align:right;border-bottom:1px solid #E0E0E0;background-color:{bg};">'
                f"{_cell_txt(r['hoje'])}</td>"
                f'<td style="padding:8px 10px;font-family:Arial,sans-serif;font-size:13px;'
                f"text-align:right;border-bottom:1px solid #E0E0E0;background-color:{bg};"
                f'font-weight:bold;color:{var_color};">'
                f"{_cell_txt(r['var'])}</td>"
                "</tr>"
            )
        body = "\n".join(parts)

    rank_header = ""
    if show_ranking:
        rank_header = (
            '<th style="padding:8px 10px;text-align:right;font-family:Arial,sans-serif;'
            'font-size:12px;font-weight:bold;color:#000;border-bottom:1px solid #BDBDBD;">'
            "Ranking</th>"
        )

    return f"""
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:900px;margin-bottom:24px;border-collapse:collapse;">
  <tr>
    <td style="background-color:{title_bg};color:#FFFFFF;font-family:Arial,sans-serif;font-size:15px;font-weight:bold;padding:10px 12px;">
      {icon} {html.escape(title, quote=True)}
    </td>
  </tr>
  <tr>
    <td style="padding:0;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
        <tr style="background-color:{header_row_bg};">
          {rank_header}
          <th style="padding:8px 10px;text-align:left;font-family:Arial,sans-serif;font-size:12px;font-weight:bold;color:#000;border-bottom:1px solid #BDBDBD;">Descrição</th>
          <th style="padding:8px 10px;text-align:right;font-family:Arial,sans-serif;font-size:12px;font-weight:bold;color:#000;border-bottom:1px solid #BDBDBD;">Ontem</th>
          <th style="padding:8px 10px;text-align:right;font-family:Arial,sans-serif;font-size:12px;font-weight:bold;color:#000;border-bottom:1px solid #BDBDBD;">Hoje</th>
          <th style="padding:8px 10px;text-align:right;font-family:Arial,sans-serif;font-size:12px;font-weight:bold;color:#000;border-bottom:1px solid #BDBDBD;">Variação</th>
        </tr>
        {body}
      </table>
    </td>
  </tr>
</table>
""".strip()


def build_html_email(
    aumentos: list[dict],
    reducoes: list[dict],
    empresa_label: str | None = None,
    ultima_compra_html: str | None = None,
) -> str:
    show_rank = (bool(aumentos) and "rn" in aumentos[0]) or (
        bool(reducoes) and "rn" in reducoes[0]
    )
    t_red = _build_table(
        "Reduções Significativas",
        title_bg="#1565C0",
        header_row_bg="#E3F2FD",
        rows=reducoes,
        var_positive=False,
        show_ranking=show_rank,
    )
    t_aum = _build_table(
        "Aumentos Significativos",
        title_bg="#C62828",
        header_row_bg="#FFEBEE",
        rows=aumentos,
        var_positive=True,
        show_ranking=show_rank,
    )
    lead = "Relatório de variação de preços"
    if empresa_label:
        lead += f" — {html.escape(empresa_label, quote=True)}"
    extra = ultima_compra_html or ""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="utf-8"><title>Tracking</title></head>
<body style="margin:0;padding:16px;background-color:#FAFAFA;">
  <div style="max-width:920px;margin:0 auto;background-color:#FFFFFF;padding:20px;border-radius:4px;">
    <p style="font-family:Arial,sans-serif;font-size:14px;color:#333;margin:0 0 16px 0;">
      {lead}
    </p>
    {extra}
    {t_red}
    {t_aum}
  </div>
</body>
</html>
"""


def _smtp_from_env() -> dict:
    """Preenche settings de e-mail a partir do .env se ainda não estiverem no Django."""
    mapping = {
        "EMAIL_HOST": "EMAIL_HOST",
        "EMAIL_PORT": "EMAIL_PORT",
        "EMAIL_HOST_USER": "EMAIL_HOST_USER",
        "EMAIL_HOST_PASSWORD": "EMAIL_HOST_PASSWORD",
        "DEFAULT_FROM_EMAIL": "DEFAULT_FROM_EMAIL",
    }
    for key, envk in mapping.items():
        v = os.getenv(envk)
        if v is not None and str(v).strip() != "":
            if key == "EMAIL_PORT":
                setattr(settings, key, int(v))
            else:
                setattr(settings, key, v.strip().strip('"'))

    use_ssl = os.getenv("EMAIL_USE_SSL", "").lower() in ("1", "true", "yes")
    use_tls = os.getenv("EMAIL_USE_TLS", "").lower() in ("1", "true", "yes")
    settings.EMAIL_USE_SSL = use_ssl
    settings.EMAIL_USE_TLS = use_tls and not use_ssl


def send_tracking_email(html_body: str, to_emails: list[str], subject: str | None = None) -> None:
    _smtp_from_env()
    subject = subject or os.getenv(
        "TRACKING_EMAIL_SUBJECT",
        "Relatório — Tracking de preços",
    )
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or settings.EMAIL_HOST_USER
    if not from_email:
        raise RuntimeError("DEFAULT_FROM_EMAIL ou EMAIL_HOST_USER não configurado.")

    msg = EmailMultiAlternatives(
        subject=subject,
        body="Este e-mail requer um cliente que suporte HTML.",
        from_email=from_email,
        to=to_emails,
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)


def _tracking_email_override_list(email_to: str | None) -> list[str]:
    """Lista de e-mails fixos: `email_to` (ex.: CLI --to) ou TRACKING_EMAIL_TO no .env."""
    if email_to is not None and str(email_to).strip():
        raw = str(email_to).strip()
    else:
        raw = os.getenv("TRACKING_EMAIL_TO", "") or ""
    return [e.strip() for e in raw.split(",") if e.strip()]


def run_relatorio_tracking_job(
    *,
    dry_run: bool = False,
    email_to: str | None = None,
    subject: str | None = None,
    cli_per_empresa: bool = False,
) -> int:
    """
    Envia o relatório de tracking (mesma regra que a CLI, sem --show-columns).
    Para Django-Q2: ``RH.tasks_tracking.enviar_relatorio_tracking_precos`` chama isto
    sem argumentos (usa só `.env` / `TRACKING_*`).

    Retorna 0 em sucesso, 1 se não houver destinatários ou dry-run sem erro.
    """
    per_empresa = cli_per_empresa or _env_bool("TRACKING_PER_EMPRESA")
    to_override = _tracking_email_override_list(email_to)
    base_subject = subject or os.getenv(
        "TRACKING_EMAIL_SUBJECT",
        "Relatório — Tracking de preços",
    )

    if per_empresa:
        data = fetch_tracking_rows(per_empresa=True)
        if not isinstance(data, dict):
            raise RuntimeError("fetch_tracking_rows(per_empresa=True) deveria devolver dict.")
        if dry_run:
            for emp_key, bundle in sorted(data.items(), key=lambda x: x[0]):
                print(f"\n<!-- ===== Empresa {html.escape(str(emp_key), quote=True)} ===== -->\n")
                print(
                    build_html_email(
                        bundle["aumentos"],
                        bundle["reducoes"],
                        empresa_label=bundle["label"],
                        ultima_compra_html=_ultima_registro_html_single(
                            bundle.get("ultima_data")
                        ),
                    )
                )
            return 0
        sent = 0
        for emp_key, bundle in sorted(data.items(), key=lambda x: x[0]):
            to_list = to_override if to_override else _recipient_emails_for_empresa(emp_key)
            if not to_list:
                print(
                    f"Aviso: sem destinatário para empresa {bundle['label']!r} (chave {emp_key!r}); ignorada.",
                    file=sys.stderr,
                )
                continue
            html_out = build_html_email(
                bundle["aumentos"],
                bundle["reducoes"],
                empresa_label=bundle["label"],
                ultima_compra_html=_ultima_registro_html_single(bundle.get("ultima_data")),
            )
            subj = base_subject
            if not subject:
                subj = f"{base_subject} — {bundle['label']}"
            send_tracking_email(html_out, to_list, subject=subj)
            print(f"E-mail enviado ({bundle['label']}): {', '.join(to_list)}")
            sent += 1
        if sent == 0:
            print("Nenhum e-mail enviado (sem destinatários por empresa).", file=sys.stderr)
            return 1
        return 0

    triple = fetch_tracking_rows(per_empresa=False)
    if not isinstance(triple, tuple) or len(triple) != 4:
        raise RuntimeError(
            "fetch_tracking_rows(per_empresa=False) deve devolver (aumentos, reducoes, emp_keys, ultima_html)."
        )
    aumentos, reducoes, emp_keys, ultima_html = triple
    html_out = build_html_email(
        aumentos, reducoes, ultima_compra_html=ultima_html
    )

    if dry_run:
        print(html_out)
        return 0

    if to_override:
        to_list = to_override
    else:
        to_list = _recipients_for_empresa_keys_aggregate(emp_keys)
    if not to_list:
        print(
            "Sem destinatários: defina --to ou TRACKING_EMAIL_TO; ou cadastre RH.EmailRelatorio "
            "(relatorio_tracking=S) ligado às empresas que aparecem na view (mapeie a coluna EMPRESA no .env).",
            file=sys.stderr,
        )
        return 1

    send_tracking_email(html_out, to_list, subject=base_subject)
    print(f"E-mail enviado para: {', '.join(to_list)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Relatório VW_TRACKING por e-mail.")
    parser.add_argument(
        "--to",
        dest="to",
        help="Destinatário(s) fixos (opcional), separados por vírgula. Se omitido, usa-se RH.EmailRelatorio "
        "das empresas do relatório (coluna EMPRESA na view) ou TRACKING_EMAIL_TO no .env.",
    )
    parser.add_argument("--subject", help="Assunto do e-mail.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Só gera o HTML no stdout, sem enviar e-mail.",
    )
    parser.add_argument(
        "--show-columns",
        action="store_true",
        help="Lista colunas da view (metadados) e o mapeamento inferido; não envia e-mail.",
    )
    parser.add_argument(
        "--per-empresa",
        action="store_true",
        help="Um e-mail por empresa (TRACKING_PER_EMPRESA no .env também ativa).",
    )
    args = parser.parse_args(argv)

    if args.show_columns:
        view = VIEW_NAME.strip()
        colnames = fetch_view_column_names(view)
        mapping = infer_column_mapping(colnames)
        print(format_mapping_report(colnames, mapping))
        return 0

    return run_relatorio_tracking_job(
        dry_run=args.dry_run,
        email_to=args.to,
        subject=args.subject,
        cli_per_empresa=args.per_empresa,
    )


if __name__ == "__main__":
    raise SystemExit(main())
