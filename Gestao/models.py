from django.db import models
from RH.models import Empresa
from django.contrib.auth.models import User


NATUREZA = [
    ('Saida','Saida'),
    ('Entrada','Entrada')
]

TIPO_OPERACAO = [
    ('DRE','DRE'),
    ('DFC','DFC'),
    ('Todas','Todas')
]


class CentroCusto(models.Model):
    codigo = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Centro de Custo'
        verbose_name_plural = 'Centros de Custo'
        db_table = 'gestao_centrocusto'
    
    def __str__(self):
        return self.nome
    

class Dre(models.Model):
    codigo = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    nivel = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.nivel
    
    def save(self, *args, **kwargs):
        self.nivel = self.codigo +' - '+ self.nome
        super(Dre, self).save(*args,**kwargs)
    
    

class Dfc(models.Model):
    codigo = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    dfc = models.CharField(max_length=100)
    nivel1 = models.CharField(max_length=100, null=True, blank=True)
    nivel2 = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.dfc
    
    def save(self, *args, **kwargs):
        self.dfc = self.codigo +' - '+ self.nome
        super(Dfc, self).save(*args,**kwargs)    
    
class Conta(models.Model):
    codigo  = models.CharField(max_length=10, unique=True)  # Código único para cada conta
    nome    = models.CharField(max_length=100)
    mae     = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='filhos')
    nivel_dre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='filhosDre')
    nivel   = models.IntegerField(default=0, null=True, blank=True)
    solucao = models.CharField(max_length=10,null=True, blank=True)
    dre     = models.ForeignKey(Dre, on_delete=models.SET_NULL, null=True, blank=True) # Nivel hierárquico da conta (0 para o topo)
    natureza = models.CharField(max_length=30, choices=NATUREZA, null=True, blank=True)
    analitica = models.BooleanField(default=False, null=True, blank=True)
    ordem = models.CharField(max_length=30, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    operacao = models.CharField(max_length=30, default='Todas', choices=TIPO_OPERACAO)
    dfc = models.ForeignKey(Dfc, on_delete=models.SET_NULL, null=True, blank=True)
    cenario = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.codigo +' - '+ self.nome
    
    def save(self, *args, **kwargs):
        self.nivel = self.codigo.count('.') + 1
        self.ordem = '0'+str(self.codigo).replace('.','')
        
        if self.nivel > 1:
            index = self.codigo.rfind('.')
            self.mae = Conta.objects.get(codigo=self.codigo[0:index])
        
        if self.dre:
            print("update gestao_conta set dre_id = %s WHERE nome LIKE %s", [self.dre.id, f'{self.codigo}%'])
            # Conta.objects.raw("update gestao_conta set dre_id = %s WHERE codigo LIKE %s", [self.dre.id, f'%{self.codigo}%'])
            Conta.objects.filter(codigo__startswith=self.codigo).update(dre=self.dre.id)
            
        
            
        super(Conta, self).save(*args,**kwargs)
    
    
class Orcamento(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    data = models.DateField()
    conta = models.ForeignKey(Conta, on_delete=models.PROTECT)
    valor = models.FloatField(default=0)
    pessimista = models.FloatField(default=0)
    otimista = models.FloatField(default=0)
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.PROTECT, null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.empresa.empresa +' - '+ str(self.data) +' - '+ self.conta.nome


class Lancamento(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    data = models.DateField()
    conta = models.ForeignKey(Conta, on_delete=models.PROTECT)
    valor = models.FloatField(default=0)
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.empresa.empresa +' - '+ str(self.data) +' - '+ self.conta.nome
    

class Banco(models.Model):
    banco = models.CharField(max_length=50)
    
    def __str__(self):
        return self.banco
    
    
class Conta_Financeira(models.Model):
    conta = models.ForeignKey(Banco, on_delete=models.PROTECT)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    data = models.DateField()
    saldo_inicial = models.FloatField()
    
    def __str__(self):
        return self.conta.banco
    
    
class ConfigGeral(models.Model):
    parametro = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        verbose_name = 'Configuração Geral'
        verbose_name_plural = 'Configurações Gerais'

    
    def __str__(self):
        return self.parametro +' - '+ self.valor

    
    
class Fornecedor(models.Model):
    codigo = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.codigo +' - '+ self.nome
    
    