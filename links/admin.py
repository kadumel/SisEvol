from django.contrib import admin
from .models import Acesso, Link, Tarefa
from links.tasks import somar, executar_job_pentaho
from datetime import datetime
# Register your models here.

admin.site.register(Acesso)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id','empresa','desc','link')
    list_filter = ('desc','link')
    search_fields = ('desc',)

from django.utils.translation import gettext_lazy as _

# Personalizando o título e o cabeçalho
admin.site.site_header = _('Grupo Evol')
admin.site.site_title = _('Grupo Evol')
admin.site.index_title = _('Administração')


def ExecutarTarefa(ModelAdmin, request, queryset):

    for i in queryset:
        i.status_processo = 'E'
        i.inicio = datetime.now()
        i.fim = None
        i.save()
        executar_job_pentaho.delay(i.id, i.path)

    
ExecutarTarefa.short_description = 'Executar Tarefas !!!'


@admin.register(Tarefa)
class TarefasAdmin(admin.ModelAdmin):
    fields = ('nome', 'path', 'status_tarefa','tipo', 'grupo')
    list_display = ('id','nome','tipo','grupo','status_tarefa', 'status_processo', 'dt_formatada_inicio', 'dt_formatada_fim')
    list_filter = ('tipo','grupo')
    search_fields = ('nome',)
    actions = (ExecutarTarefa,)
    
    def dt_formatada_inicio(self, obj):
    # Formatar a data exibida na lista do admin
        if obj.inicio:
            return obj.inicio.strftime('%d/%m/%Y %H:%M:%S')
        else:
            return None

    dt_formatada_inicio.admin_order_field = 'inicio'  # Permite ordenar por 'inicio'
    dt_formatada_inicio.short_description = 'Data de Início'



    def dt_formatada_fim(self, obj):
    # Formatar a data exibida na lista do admin
        if obj.fim:
            return obj.fim.strftime('%d/%m/%Y %H:%M:%S')
        else:
            return None

    dt_formatada_fim.admin_order_field = 'fim'  # Permite ordenar por 'inicio'
    dt_formatada_fim.short_description = 'Data de Fim'

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'js/admin.js',)    
        
        