from django.core.management.base import BaseCommand
from cardapio.models import Prato, Categoria


class Command(BaseCommand):
    help = 'Lista pratos importados do PDF'

    def add_arguments(self, parser):
        parser.add_argument(
            '--categoria',
            type=str,
            help='Filtrar por categoria'
        )
        parser.add_argument(
            '--detalhes',
            action='store_true',
            help='Mostrar detalhes completos dos pratos'
        )

    def handle(self, *args, **options):
        categoria_filtro = options.get('categoria')
        mostrar_detalhes = options.get('detalhes')
        
        pratos = Prato.objects.all()
        
        if categoria_filtro:
            pratos = pratos.filter(categoria__nome__icontains=categoria_filtro)
        
        self.stdout.write(f'Total de pratos encontrados: {pratos.count()}')
        self.stdout.write('=' * 50)
        
        for prato in pratos:
            self.stdout.write(f'\n🍽️  {prato.nome}')
            self.stdout.write(f'   Categoria: {prato.categoria.nome}')
            self.stdout.write(f'   Preço: R$ {prato.preco:.2f}')
            
            if prato.descricao:
                self.stdout.write(f'   Descrição: {prato.descricao[:100]}...')
            
            if mostrar_detalhes:
                if prato.ingredientes:
                    self.stdout.write(f'   Ingredientes: {prato.ingredientes[:100]}...')
                
                if prato.quantitativo_ingredientes:
                    self.stdout.write(f'   Quantitativo: {prato.quantitativo_ingredientes[:100]}...')
                
                if prato.modo_preparo:
                    self.stdout.write(f'   Modo de Preparo: {prato.modo_preparo[:100]}...')
                
                if prato.montagem_prato:
                    self.stdout.write(f'   Montagem: {prato.montagem_prato[:100]}...')
                
                if prato.utensilios_necessarios:
                    self.stdout.write(f'   Utensílios: {prato.utensilios_necessarios[:100]}...')
                
                self.stdout.write(f'   Calorias: {prato.calorias}')
                self.stdout.write(f'   Tempo: {prato.tempo_preparo} min')
                self.stdout.write(f'   Dificuldade: {prato.dificuldade_display}')
                self.stdout.write(f'   Rendimento: {prato.rendimento}')
                self.stdout.write(f'   Temperatura: {prato.temperatura_servico}')
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('Resumo por categoria:')
        
        for categoria in Categoria.objects.all():
            count = categoria.pratos.count()
            self.stdout.write(f'  {categoria.nome}: {count} pratos')
