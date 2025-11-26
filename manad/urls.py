from django.urls import path
from . import views

urlpatterns = [
    path('manad/', views.IndexManadView.as_view(), name='indexManad'),
    path('manad/importacoes/', views.ListImportacoesView.as_view(), name='listImportacoesManad'),
    path('manad/importar/', views.ImportarManadView.as_view(), name='importarManad'),
]

