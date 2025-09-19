from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Prato

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cor_preview', 'ordem', 'ativo', 'created_at']
    list_filter = ['ativo', 'created_at']
    search_fields = ['nome', 'descricao']
    ordering = ['ordem', 'nome']
    list_editable = ['ordem', 'ativo']
    
    def cor_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px; display: inline-block;"></div> {}',
            obj.cor, obj.cor
        )
    cor_preview.short_description = 'Cor'

@admin.register(Prato)
class PratoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'tamanho', 'destaque', 'ativo', 'created_at']
    list_filter = ['categoria', 'tamanho', 'vegetariano', 'vegano', 'sem_gluten', 'sem_lactose', 'destaque', 'ativo', 'created_at']
    search_fields = ['nome', 'descricao', 'ingredientes']
    ordering = ['categoria__ordem', 'categoria__nome', 'nome']
    list_editable = ['destaque', 'ativo']
    filter_horizontal = []
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('categoria', 'nome', 'descricao', 'ingredientes', 'preco', 'tamanho')
        }),
        ('Características', {
            'fields': ('calorias', 'tempo_preparo', 'nivel_picante')
        }),
        ('Ficha Técnica', {
            'fields': ('rendimento', 'tempo_preparo_total', 'dificuldade', 'temperatura_servico', 'utensilios_necessarios', 'quantitativo_ingredientes', 'modo_preparo', 'montagem_prato', 'dicas_chef', 'conservacao', 'valor_nutricional'),
            'classes': ('collapse',)
        }),
        ('Restrições Alimentares', {
            'fields': ('vegetariano', 'vegano', 'sem_gluten', 'sem_lactose'),
            'classes': ('collapse',)
        }),
        ('Mídia e Status', {
            'fields': ('imagem', 'destaque', 'ativo')
        }),
    )

