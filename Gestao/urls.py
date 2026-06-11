from django.urls import path
from . import views

app_name = 'gestao'

urlpatterns = [
    path('orcamento/update_valor/', views.update_orcamento_valor, name='update_orcamento_valor'),
    path('orcamento/',  views.DreOrcadoView.as_view(), name='orcamento_menu'),
    path('orcamento/visualizacao/', views.OrcamentoVisualizacaoView.as_view(), name='orcamento_visualizacao'),
    path('orcamento/dre-orcado/', views.DreOrcadoView.as_view(), name='dre_orcado'),
    path('orcamento/export-excel/', views.ExportOrcamentoExcelView.as_view(), name='orcamento_export_excel'),
    path('orcamento/importar-xlsx/', views.ImportarOrcamentoXlsxView.as_view(), name='orcamento_importar_xlsx'),
    path('orcamento/importar-xlsx/modelo/', views.DownloadModeloOrcamentoXlsxView.as_view(), name='orcamento_modelo_xlsx'),
] 