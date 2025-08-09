from django.db import models
from django.contrib.auth.models import User, Group
from RH.models import Empresa

# Create your models here.



class Link(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    desc = models.CharField(max_length=40, default='')
    link = models.CharField(max_length=400)
    
    class Meta:
        # Managed = True
        db_table = 'Link'

    def __str__(self):
        return '{} - {} '.format(self.empresa.empresa, self.desc)

class Acesso(models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    link = models.ForeignKey(Link, on_delete=models.PROTECT)

    class Meta:
        db_table = 'Acesso'
        ordering = ['group__name']

    def __str__(self):
        return f'{self.group.name} - {self.link.desc}'


class Tarefa(models.Model):
    STATUS_TAREFA = (
        ('E','Habilitado'),
        ('D','Desabilitado')
    )

    STATUS_PROCESSO = (
        ('E','Executando'),
        ('P','Parado'),
        ('S','Finalizado'),
        ('F','Falhou')
    )
    
    TIPO = (
        ('GERAL','GERAL'),
        ('INDIVIDUAL','INDIVIDUAL')
    )
    
    GRUPO_TAREFA = (
        ('FINANCEIRO','FINANCEIRO'),
        ('VENDAS','VENDAS'),
        ('DIMENSOES','DIMENSOES'),
        ('COMPRAS','COMPRAS'),
    )

    nome = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    status_tarefa = models.CharField(choices=STATUS_TAREFA, null=True, blank=True, max_length=50)
    status_processo = models.CharField(choices=STATUS_PROCESSO, null=True, blank=True, max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    inicio = models.DateTimeField(null=True, blank=True)
    fim = models.DateTimeField(null=True, blank=True) 
    tipo = models.CharField(null=True, blank=True, choices=TIPO, max_length=30)
    grupo = models.CharField(max_length=50, null=True, blank=True, choices=GRUPO_TAREFA)
    

    def __str__(self):
        return self.nome
