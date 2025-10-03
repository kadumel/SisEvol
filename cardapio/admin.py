from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria,  FichaTecnicaProduto, FichaTecnica, Produto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'icone', 'cor_preview', 'tempo_preparo', 'ordem', 'ativo', 'created_at']
    list_filter = ['ativo', 'created_at']
    search_fields = ['nome', 'descricao']
    ordering = ['ordem', 'nome']
    list_editable = ['ordem', 'ativo', 'tempo_preparo']
    
    def cor_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px; display: inline-block;"></div> {}',
            obj.cor, obj.cor
        )
    cor_preview.short_description = 'Cor'


@admin.register(FichaTecnicaProduto)
class FichaTecnicaProdutoAdmin(admin.ModelAdmin):
    list_display = ['ficha_tecnica_prato', 'ficha_tecnica_categoria', 'produto', 'med_caseira', 'quantidade', 'unidade']
    list_filter = ['ficha_tecnica__categoria']
    search_fields = ['ficha_tecnica__prato', 'produto__nome']
    ordering = ['ficha_tecnica__prato', 'produto']

    def ficha_tecnica_prato(self, obj):
        return obj.ficha_tecnica.prato if obj.ficha_tecnica else ''
    ficha_tecnica_prato.short_description = 'Ficha Técnica'

    def ficha_tecnica_categoria(self, obj):
        return obj.ficha_tecnica.categoria if obj.ficha_tecnica and obj.ficha_tecnica.categoria else ''
    ficha_tecnica_categoria.short_description = 'Categoria'
    
    
@admin.register(FichaTecnica)
class FichaTecnicaAdmin(admin.ModelAdmin):
    list_display = ['prato', 'categoria', 'descricao', 'imagem_preview', 'modo_preparo']
    list_filter = ['categoria']
    search_fields = ['prato', 'categoria__nome']
    ordering = ['categoria', 'prato']
    readonly_fields = ['imagem_preview']
    list_editable = ['categoria']
    fields = ['prato', 'categoria', 'descricao', 'modo_preparo', 'imagem', 'imagem_preview']

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="max-height: 120px;" />', obj.imagem.url)
        return "—"
    imagem_preview.short_description = 'Preview'


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_filter = ['nome']
    search_fields = ['nome']
    ordering = ['nome']
    
    
