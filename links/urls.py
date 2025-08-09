from django.urls import path
# from django.views.generic import TemplateView

from . import views


urlpatterns = [
    # path("", views.indexLinks),
    path('', views.indexLinks, name='indexLinks'),
    path('painel/<int:id>', views.painel, name='painel'),
    path('status_tarefa', views.verificar_status_tarefa.as_view(), name='verificar_status_tarefa'),

]
   

