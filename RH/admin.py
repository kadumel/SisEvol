from django.contrib import admin
from .models import Cargo, Empresa, TipoContrato, Banco, Lotacao, Turno, Vaga, Funcionario, Gestor, ConfigGeral, Auditoria, TipoEvento, Evento, ControleEvento, DiaEvento, FrequenciaEvento
from .admin_mixins import DateHierarchyCurrentMonthMixin

# Register your models here.
@admin.register(ConfigGeral)
class ConfigGeralAdmin(admin.ModelAdmin):
    list_display = ('empresa','dias_primeiro_termino_exp','dias_segundo_termino_exp')


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['codigo_BI','empresa']


@admin.register(DiaEvento)
class DiaEventoAdmin(DateHierarchyCurrentMonthMixin, admin.ModelAdmin):
    list_display = ['evento', 'data', 'hora_inicio', 'hora_fim']
    list_filter = ['evento__tipo']
    search_fields = ['evento__descricao', 'local']
    date_hierarchy = 'data'
    
    class Media:
        js = ('js/adminRH.js',)


@admin.register(FrequenciaEvento)
class FrequenciaEventoAdmin(DateHierarchyCurrentMonthMixin, admin.ModelAdmin):
    list_display = ['controle_evento', 'dia_evento', 'status', 'hora_entrada', 'hora_saida', 'usuario_registro']
    list_filter = ['status', 'dia_evento__evento__tipo', 'dia_evento__data']
    search_fields = ['controle_evento__funcionario__nome', 'controle_evento__funcionario__matricula']
    date_hierarchy = 'dia_evento__data'
    list_editable = ['status']
    
    class Media:
        js = ('js/adminRH.js',)


admin.site.register(Cargo)
admin.site.register(TipoContrato)
admin.site.register(Banco)
admin.site.register(Lotacao)
admin.site.register(Turno)
admin.site.register(Vaga)
admin.site.register(Funcionario)
admin.site.register(Gestor)

admin.site.register(TipoEvento)
admin.site.register(Evento)
admin.site.register(ControleEvento)
admin.site.register(Auditoria)


