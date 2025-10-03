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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordem', 'nome']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome

class Prato(models.Model):
    TAMANHO_CHOICES = [
        ('P', 'Pequeno'),
        ('M', 'Médio'),
        ('G', 'Grande'),
        ('U', 'Único'),
    ]

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='pratos')
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    ingredientes = models.TextField(help_text='Lista de ingredientes separados por vírgula')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tamanho = models.CharField(max_length=1, choices=TAMANHO_CHOICES, default='U')
    calorias = models.PositiveIntegerField(blank=True, null=True, help_text='Calorias aproximadas')
    tempo_preparo = models.PositiveIntegerField(blank=True, null=True, help_text='Tempo de preparo em minutos')
    nivel_picante = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text='Nível de picante de 0 a 5'
    )
    vegetariano = models.BooleanField(default=False)
    vegano = models.BooleanField(default=False)
    sem_gluten = models.BooleanField(default=False)
    sem_lactose = models.BooleanField(default=False)
    imagem = models.ImageField(upload_to='pratos/', blank=True, null=True, help_text='Imagem do prato')
    destaque = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    
    # Campos da Ficha Técnica
    rendimento = models.CharField(max_length=50, blank=True, null=True, help_text='Ex: 4 porções, 1 unidade')
    tempo_preparo_total = models.PositiveIntegerField(blank=True, null=True, help_text='Tempo total de preparo em minutos')
    dificuldade = models.CharField(max_length=20, choices=[
        ('facil', 'Fácil'),
        ('medio', 'Médio'),
        ('dificil', 'Difícil'),
    ], default='facil')
    temperatura_servico = models.CharField(max_length=50, blank=True, null=True, help_text='Ex: Quente, Frio, Morno')
    utensilios_necessarios = models.TextField(blank=True, null=True, help_text='Lista de utensílios necessários')
    quantitativo_ingredientes = models.TextField(blank=True, null=True, help_text='Quantidades específicas dos ingredientes')
    modo_preparo = models.TextField(blank=True, null=True, help_text='Instruções detalhadas de preparo')
    montagem_prato = models.TextField(blank=True, null=True, help_text='Instruções de montagem e apresentação do prato')
    dicas_chef = models.TextField(blank=True, null=True, help_text='Dicas especiais do chef')
    conservacao = models.TextField(blank=True, null=True, help_text='Instruções de conservação')
    valor_nutricional = models.TextField(blank=True, null=True, help_text='Informações nutricionais detalhadas')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['categoria__ordem', 'categoria__nome', 'nome']
        verbose_name = 'Prato'
        verbose_name_plural = 'Pratos'

    def __str__(self):
        return f"{self.nome} - {self.categoria.nome}"

    @property
    def ingredientes_list(self):
        """Retorna lista de ingredientes"""
        return [ing.strip() for ing in self.ingredientes.split(',') if ing.strip()]

    @property
    def nivel_picante_display(self):
        """Retorna representação visual do nível de picante"""
        return '🌶️' * self.nivel_picante
    
    @property
    def dificuldade_display(self):
        """Retorna representação visual da dificuldade"""
        dificuldades = {
            'facil': '🟢 Fácil',
            'medio': '🟡 Médio', 
            'dificil': '🔴 Difícil'
        }
        return dificuldades.get(self.dificuldade, 'Fácil')
    
    @property
    def utensilios_list(self):
        """Retorna lista de utensílios"""
        if self.utensilios_necessarios:
            return [ut.strip() for ut in self.utensilios_necessarios.split(',') if ut.strip()]
        return []
    
    @property
    def modo_preparo_list(self):
        """Retorna lista de passos do modo de preparo"""
        if self.modo_preparo:
            return [passo.strip() for passo in self.modo_preparo.split('\n') if passo.strip()]
        return []
    
    @property
    def quantitativo_ingredientes_list(self):
        """Retorna lista de ingredientes com quantidades"""
        if self.quantitativo_ingredientes:
            return [item.strip() for item in self.quantitativo_ingredientes.split('\n') if item.strip()]
        return []
    
    @property
    def montagem_prato_list(self):
        """Retorna lista de passos da montagem"""
        if self.montagem_prato:
            return [passo.strip() for passo in self.montagem_prato.split('\n') if passo.strip()]
        return []

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
    