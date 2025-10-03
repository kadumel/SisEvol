from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from decimal import Decimal

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    icone = models.CharField(max_length=50, default='bi-utensils')
    cor = models.CharField(max_length=7, default='#667eea', help_text='Cor em hexadecimal (ex: #667eea)')
    ordem = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    tempo_preparo = models.PositiveIntegerField(default=0, help_text='Tempo de preparo em minutos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordem', 'nome']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


class FichaTecnica(models.Model):
    prato = models.CharField(max_length=200, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='ficha_tecnica', null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    modo_preparo = models.TextField(null=True, blank=True)
    imagem = models.ImageField(upload_to='fichas_tecnicas/', null=True, blank=True, help_text='Imagem da ficha técnica')
    
    class Meta:
        verbose_name = 'Ficha Técnica'
        verbose_name_plural = 'Fichas Técnicas'
        db_table = 'cardapio_ficha_tecnica'

    
    
class Produto(models.Model):
    nome = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        db_table = 'cardapio_produto'

    def __str__(self):
        return self.nome
    
    
class FichaTecnicaProduto(models.Model):
    ficha_tecnica = models.ForeignKey(FichaTecnica, on_delete=models.CASCADE, related_name='ficha_tecnica_produto')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='ficha_tecnica_produto')
    med_caseira = models.CharField(max_length=200, null=True, blank=True)
    quantidade = models.CharField(max_length=20, null=True, blank=True)
    unidade = models.CharField(max_length=20, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Ficha Técnica Produto'
        verbose_name_plural = 'Fichas Técnicas Produtos'
        db_table = 'cardapio_ficha_produto'

    def __str__(self):
        return self.produto.nome
    