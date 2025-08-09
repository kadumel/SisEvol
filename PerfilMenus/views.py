from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .models import Menu, AcaoTipo, Acao, PermissaoGrupo

# Create your views here.


def AcessoAcoes(request, menu_nome, acao_nome):
    grupo = User.objects.filter(username=request.user).values('groups')
    print('grupo:', grupo)
    
    # acessos  = PerfilMenu.objects.filter(group__in=groups).values_list('link', flat=True)
    try:
        menu = Menu.objects.get(nome=menu_nome)
        print('menus:', menu)
        acao_tipo = AcaoTipo.objects.get(nome=acao_nome)
        print('acao_tipo:', acao_tipo)
        acao = Acao.objects.get(menu=menu, acao=acao_tipo)
        print('acao:', acao)
        
        resultado = PermissaoGrupo.objects.filter(grupo__in=grupo, acao=acao)
        print('resultado:', resultado)
        return resultado.exists()  # Retorna True se existir permissão, False caso contrário
    except Exception as e:
        print('erro:', e)
        return False
