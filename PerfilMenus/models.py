from django.db import models
from django.contrib.auth.models import Group

class Menu(models.Model):
    nome = models.CharField(max_length=50, default='teste')
    url = models.CharField(max_length=200, blank=True, null=True)
    pai = models.ForeignKey('self', null=True, blank=True, related_name='submenus', on_delete=models.CASCADE)

    class Meta:
        ordering = ['nome']
        db_table = 'menu'

    def __str__(self):
        return self.nome


class AcaoTipo(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        db_table = 'acao_tipo'

    def __str__(self):
        return self.nome


class Acao(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    acao = models.ForeignKey(AcaoTipo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('menu', 'acao')
        db_table = 'acao'

    def __str__(self):
        return f'{self.menu.nome} - {self.acao.nome}'


class PermissaoGrupo(models.Model):
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE)
    acao = models.ForeignKey(Acao, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('grupo', 'acao')
        db_table = 'permissao_grupo'

    def __str__(self):
        return f'{self.grupo.name} pode {self.acao.acao.nome} em {self.acao.menu.nome}'
