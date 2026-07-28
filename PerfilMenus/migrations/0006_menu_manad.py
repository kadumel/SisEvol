from django.db import migrations


ACOES_MANAD = ['Listar', 'Inserir', 'Consultar', 'Deletar']


def criar_menu_manad(apps, schema_editor):
    Menu = apps.get_model('PerfilMenus', 'Menu')
    AcaoTipo = apps.get_model('PerfilMenus', 'AcaoTipo')
    Acao = apps.get_model('PerfilMenus', 'Acao')

    menu, _ = Menu.objects.get_or_create(
        nome='MANAD',
        defaults={'url': 'manad/'},
    )

    for acao_nome in ACOES_MANAD:
        acao_tipo, _ = AcaoTipo.objects.get_or_create(nome=acao_nome)
        Acao.objects.get_or_create(menu=menu, acao=acao_tipo)


def remover_menu_manad(apps, schema_editor):
    Menu = apps.get_model('PerfilMenus', 'Menu')
    Acao = apps.get_model('PerfilMenus', 'Acao')

    menu = Menu.objects.filter(nome='MANAD').first()
    if not menu:
        return

    Acao.objects.filter(menu=menu).delete()
    menu.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('PerfilMenus', '0005_acaotipo_remove_acoes_link_acao_and_more'),
    ]

    operations = [
        migrations.RunPython(criar_menu_manad, remover_menu_manad),
    ]
