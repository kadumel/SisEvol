"""
Tarefa Django-Q2: envio do relatório de tracking de preços (VW_TRACKING).

No Admin → Django Q → **Scheduled tasks**, crie uma linha com:
  - **Func:** ``RH.tasks_tracking.enviar_relatorio_tracking_precos``
  - **Schedule type:** Daily / Cron / etc.
  - **Cluster:** ``SisEvol`` (o mesmo de ``Q_CLUSTER['name']`` em ``core/settings.py``)
  - **Repeats:** -1 (para repetir indefinidamente)

O worker tem de estar a correr: ``python manage.py qcluster``

Configuração do relatório continua no ``.env`` na raiz do projeto (``TRACKING_*``,
``TRACKING_PER_EMPRESA``, SMTP, etc.), igual ao script ``RelatorioTranking.py``.
"""


def enviar_relatorio_tracking_precos() -> int:
    import RelatorioTranking as rt

    return rt.run_relatorio_tracking_job()
