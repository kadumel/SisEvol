from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Categoria, Prato



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
    
    pratos = Prato.objects.filter(
        Q(nome__icontains=query) | 
        Q(descricao__icontains=query) | 
        Q(ingredientes__icontains=query),
        ativo=True
    )[:10]
    
    resultados = []
    for prato in pratos:
        resultados.append({
            'id': prato.id,
            'nome': prato.nome,
            'categoria': prato.categoria.nome,
            'preco': float(prato.preco),
            'imagem': prato.imagem if prato.imagem else None,
        })
    
    return JsonResponse({'pratos': resultados})

def fichas_tecnicas_publicas(request):
    """Página pública de fichas técnicas - sem autenticação necessária"""
    categorias = Categoria.objects.filter(ativo=True).order_by('ordem', 'nome').prefetch_related('pratos')
    
    context = {
        'categorias': categorias,
    }
    return render(request, 'cardapio/ficha_tecnica_publica.html', context)

def ficha_tecnica_publica(request, prato_id):
    
    """Página pública individual da ficha técnica - sem autenticação necessária"""
    try:
        prato = Prato.objects.get(id=prato_id, ativo=True)
    except Prato.DoesNotExist:
        return render(request, 'cardapio/404.html', {'message': 'Prato não encontrado'})
    
    context = {
        'prato': prato,
    }
    return render(request, 'cardapio/ficha_tecnica_individual.html', context)

def ficha_tecnica_individual(request, prato_id):
    """Página individual da ficha técnica - sem autenticação necessária"""
    prato = get_object_or_404(Prato, id=prato_id, ativo=True)

    context = {
        'prato': prato,
    }
    return render(request, 'cardapio/ficha_tecnica_individual.html', context)
