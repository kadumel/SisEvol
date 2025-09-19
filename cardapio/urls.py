from django.urls import path
from . import views

app_name = 'cardapio'

urlpatterns = [
    
    path('', views.fichas_tecnicas_publicas, name='fichas_tecnicas_publicas'),
    path('categoria/<int:categoria_id>/', views.categoria_detail, name='categoria'),
    path('buscar/', views.buscar_pratos, name='buscar'),
    path('ficha-tecnica-individual/<int:prato_id>/', views.ficha_tecnica_individual, name='ficha_tecnica_individual'),
]
