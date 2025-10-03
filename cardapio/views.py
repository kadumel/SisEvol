from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Categoria, Prato, FichaTecnica, FichaTecnicaProduto
def _icon_for_categoria(nome: str) -> str:
    n = (nome or "").lower()
    # Palavras‑chave → Bootstrap Icons
    if any(k in n for k in ["entrada", "bruschetta", "pao", "camar", "polvo"]):
        return "bi-egg"
    if any(k in n for k in ["sobremesa", "sobremesas", "doce", "torta", "sorvete", "pudim", "chocolate"]):
        return "bi-cup-hot"
    if any(k in n for k in ["salada", "saladas", "folha", "veg", "burrata"]):
        return "bi-flower1"
    if any(k in n for k in ["bovino", "carne", "cortes", "steak", "picanha", "maminha", "ancho", "rib", "denver", "parrilla"]):
        return "bi-fire"
    if any(k in n for k in ["peixe", "salm", "frutos do mar", "polvo"]):
        return "bi-fish"
    if any(k in n for k in ["ave", "frango", "galetinho"]):
        return "bi-egg"
    if any(k in n for k in ["suin", "porco", "barriga", "prime rib su"]):
        return "bi-pig"
    if any(k in n for k in ["lingui", "embutido"]):
        return "bi-emoji-smile"
    if any(k in n for k in ["acompanh", "guarni", "side"]):
        return "bi-basket"
    if any(k in n for k in ["kids", "infantil"]):
        return "bi-emoji-smile"
    if any(k in n for k in ["lanche", "burger", "sand"]):
        return "bi-bag"
    if any(k in n for k in ["executivo", "prato do dia"]):
        return "bi-briefcase"
    if any(k in n for k in ["wagyu"]):
        return "bi-gem"
    if any(k in n for k in ["compartilhar", "tabua", "familia"]):
        return "bi-people"
    return "bi-grid-3x3-gap"

def _color_for_categoria(nome: str, default: str = "#667eea") -> str:
    n = (nome or "").lower()
    # Paletas aproximadas por grupo
    if any(k in n for k in ["entrada", "bruschetta", "pao", "camar", "polvo"]):
        return "#ff9800"  # laranja
    if any(k in n for k in ["sobremesa", "doce", "torta", "sorvete", "pudim", "chocolate"]):
        return "#e91e63"  # rosa
    if any(k in n for k in ["salada", "folha", "veg", "burrata"]):
        return "#4caf50"  # verde
    if any(k in n for k in ["bovino", "carne", "cortes", "steak", "picanha", "maminha", "ancho", "rib", "denver"]):
        return "#9c27b0"  # roxo
    if any(k in n for k in ["peixe", "salm", "frutos do mar"]):
        return "#03a9f4"  # azul claro
    if any(k in n for k in ["ave", "frango", "galetinho"]):
        return "#8bc34a"  # verde claro
    if any(k in n for k in ["suin", "porco", "barriga", "prime rib su"]):
        return "#795548"  # marrom
    if any(k in n for k in ["lingui", "embutido"]):
        return "#ff5722"  # laranja escuro
    if any(k in n for k in ["acompanh", "guarni", "side"]):
        return "#607d8b"  # cinza-azulado
    if any(k in n for k in ["kids", "infantil"]):
        return "#009688"  # teal
    if any(k in n for k in ["lanche", "burger", "sand"]):
        return "#ffc107"  # âmbar
    if any(k in n for k in ["executivo", "prato do dia"]):
        return "#3f51b5"  # índigo
    if any(k in n for k in ["wagyu"]):
        return "#ff5722"
    if any(k in n for k in ["compartilhar", "tabua", "familia"]):
        return "#9e9e9e"  # cinza
    return default



def categoria_detail(request, categoria_id):
    """Página de detalhes da categoria com os pratos"""
    categoria = get_object_or_404(Categoria, id=categoria_id, ativo=True)
    pratos = Prato.objects.filter(categoria=categoria, ativo=True).order_by('nome')
    
    # Filtros
    filtro_vegetariano = request.GET.get('vegetariano') == 'on'
    filtro_vegano = request.GET.get('vegano') == 'on'
    filtro_sem_gluten = request.GET.get('sem_gluten') == 'on'
    filtro_sem_lactose = request.GET.get('sem_lactose') == 'on'
    busca = request.GET.get('busca', '')
    
    if filtro_vegetariano:
        pratos = pratos.filter(vegetariano=True)
    if filtro_vegano:
        pratos = pratos.filter(vegano=True)
    if filtro_sem_gluten:
        pratos = pratos.filter(sem_gluten=True)
    if filtro_sem_lactose:
        pratos = pratos.filter(sem_lactose=True)
    if busca:
        pratos = pratos.filter(
            Q(nome__icontains=busca) | 
            Q(descricao__icontains=busca) | 
            Q(ingredientes__icontains=busca)
        )
    
    context = {
        'categoria': categoria,
        'pratos': pratos,
        'filtros': {
            'vegetariano': filtro_vegetariano,
            'vegano': filtro_vegano,
            'sem_gluten': filtro_sem_gluten,
            'sem_lactose': filtro_sem_lactose,
            'busca': busca,
        }
    }
    return render(request, 'cardapio/categoria.html', context)

def prato_detail(request, prato_id):
    """Página de detalhes do prato"""
    prato = get_object_or_404(Prato, id=prato_id, ativo=True)
    avaliacoes = Avaliacao.objects.filter(prato=prato, aprovado=True).order_by('-created_at')[:10]
    
    # Calcular média das avaliações
    if avaliacoes.exists():
        media_avaliacoes = sum(av.nota for av in avaliacoes) / avaliacoes.count()
    else:
        media_avaliacoes = 0
    
    context = {
        'prato': prato,
        'avaliacoes': avaliacoes,
        'media_avaliacoes': media_avaliacoes,
    }
    return render(request, 'cardapio/prato.html', context)

def ficha_tecnica(request, prato_id):
    """Página da ficha técnica do prato"""
    prato = get_object_or_404(Prato, id=prato_id, ativo=True)
    
    context = {
        'prato': prato,
    }
    return render(request, 'cardapio/ficha_tecnica.html', context)

def buscar_pratos(request):
    """API para busca de pratos via AJAX"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'pratos': []})
    
    fichas = FichaTecnica.objects.select_related('categoria').filter(
        Q(prato__icontains=query) |
        Q(descricao__icontains=query)
    ).order_by('prato')[:10]

    resultados = []
    for ficha in fichas:
        resultados.append({
            'id': ficha.id,
            'nome': ficha.prato,
            'categoria': ficha.categoria.nome if ficha.categoria else None,
            'imagem': ficha.imagem.url if ficha.imagem else None,
        })
    
    return JsonResponse({'pratos': resultados})

def fichas_tecnicas_publicas(request):
    """Página pública de fichas técnicas - sem autenticação necessária"""
    categorias_qs = list(Categoria.objects.filter(ativo=True).order_by('ordem', 'nome'))
    # Totais para cards resumo
    from django.db.models import Q as _Q
    total_fichas = FichaTecnica.objects.count()
    total_sem_categoria = FichaTecnica.objects.filter(
        _Q(categoria__isnull=True) | _Q(categoria__nome__iexact='geral') | _Q(categoria__nome__icontains='geral')
    ).count()
    total_sem_imagem = FichaTecnica.objects.filter(_Q(imagem__isnull=True) | _Q(imagem="")).count()

    class FakePrato:
        def __init__(self, ficha: FichaTecnica):
            self.id = ficha.id
            self.nome = ficha.prato
            self.descricao = ficha.descricao or ""
            self.calorias = 0
            self.tempo_preparo = 0
            self.imagem = ficha.imagem.url if ficha.imagem else ""
            self.vegetariano = False
            self.vegano = False
            self.sem_gluten = False
            self.sem_lactose = False

    class FakePratosManager:
        def __init__(self, items):
            self._items = items
        def all(self):
            return self._items
        def count(self):
            return len(self._items)

    class CategoriaVM:
        def __init__(self, cat: Categoria, pratos_items):
            self.id = cat.id
            self.nome = cat.nome
            self.descricao = cat.descricao
            self.icone = _icon_for_categoria(cat.nome) or cat.icone
            self.cor = _color_for_categoria(cat.nome, cat.cor)
            self.pratos = FakePratosManager(pratos_items)

    categorias_vm = []
    for categoria in categorias_qs:
        fichas = list(FichaTecnica.objects.filter(categoria=categoria).order_by('prato'))
        fake_pratos = [FakePrato(f) for f in fichas]
        categorias_vm.append(CategoriaVM(categoria, fake_pratos))

    # Categoria "Geral" para fichas sem categoria
    fichas_sem_categoria = list(FichaTecnica.objects.filter(categoria__isnull=True).order_by('prato'))
    if fichas_sem_categoria:
        class CatGeral:
            def __init__(self):
                self.id = -1
                self.nome = 'Geral'
                self.descricao = ''
                self.icone = _icon_for_categoria(self.nome)
                self.cor = _color_for_categoria(self.nome, '#667eea')
        geral = CatGeral()
        fake_pratos_geral = [FakePrato(f) for f in fichas_sem_categoria]
        categorias_vm.append(CategoriaVM(geral, fake_pratos_geral))

    context = {
        'categorias': categorias_vm,
        'total_fichas': total_fichas,
        'total_sem_categoria': total_sem_categoria,
        'total_sem_imagem': total_sem_imagem,
    }
    return render(request, 'cardapio/ficha_tecnica_publica.html', context)

def ficha_tecnica_publica(request, prato_id):
    """Página pública individual da ficha técnica - sem autenticação necessária"""
    ficha = get_object_or_404(FichaTecnica, id=prato_id)

    class FakePratoDetalhe:
        def __init__(self, ficha: FichaTecnica):
            self.id = ficha.id
            self.nome = ficha.prato
            self.categoria = ficha.categoria
            self.descricao = ficha.descricao or ""
            self.imagem = ficha.imagem.url if ficha.imagem else ""
            # Listas usadas no template
            # Quantitativo de ingredientes vindo de FichaTecnicaProduto
            itens = []
            for ftp in FichaTecnicaProduto.objects.select_related('produto').filter(ficha_tecnica=ficha):
                partes = []
                if ftp.produto and ftp.produto.nome:
                    partes.append(str(ftp.produto.nome))
                quantidade = (ftp.quantidade or "").strip()
                unidade = (ftp.unidade or "").strip()
                medida = (ftp.med_caseira or "").strip()
                quant_unid = " ".join(p for p in [quantidade, unidade] if p)
                if quant_unid:
                    partes.append(quant_unid)
                if medida:
                    partes.append(f"({medida})")
                texto = " - ".join(partes) if partes else ""
                if texto:
                    itens.append(texto)
            self.quantitativo_ingredientes_list = itens
            self.montagem_prato_list = []
            self.utensilios_list = []
            self.modo_preparo_list = [p.strip() for p in (ficha.modo_preparo or "").split('\n') if p.strip()]

    prato = FakePratoDetalhe(ficha)

    context = { 'prato': prato }
    return render(request, 'cardapio/ficha_tecnica_individual.html', context)

def ficha_tecnica_individual(request, prato_id):
    """Página individual da ficha técnica - agora baseada em FichaTecnica"""
    return ficha_tecnica_publica(request, prato_id)
