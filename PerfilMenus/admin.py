from django.contrib import admin

# Register your models here.


from .models import Menu, AcaoTipo, Acao, PermissaoGrupo


admin.site.register(AcaoTipo)



@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('nome', 'url', 'pai')
    list_filter = ('pai',)
    search_fields = ('nome', 'url')
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('url',)
    list_display_links = ('nome',)
    list_select_related = True
    
@admin.register(PermissaoGrupo)
class PermissaoGrupoAdmin(admin.ModelAdmin):
    list_display = ('grupo', 'acao')
    list_filter = ('grupo', 'acao')
    search_fields = ('grupo', 'acao')
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('acao',)
    list_display_links = ('grupo',)
    
@admin.register(Acao)
class AcaoAdmin(admin.ModelAdmin):
    list_display = ('menu', 'acao')
    list_filter = ('menu', 'acao')
    search_fields = ('menu', 'acao')
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('acao',)
    list_display_links = ('menu',)

