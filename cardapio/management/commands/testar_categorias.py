from django.core.management.base import BaseCommand
from cardapio.models import Categoria, Prato


class Command(BaseCommand):
    help = 'Testa categorias e pratos'

    def handle(self, *args, **options):
        self.stdout.write('=== CATEGORIAS ===')
        for cat in Categoria.objects.all():
            pratos_count = cat.pratos.count()
            self.stdout.write(f'{cat.nome}: {pratos_count} pratos')
            
            # Mostrar alguns pratos de cada categoria
            pratos = cat.pratos.all()[:3]
            for prato in pratos:
                self.stdout.write(f'  - {prato.nome}')
            if pratos_count > 3:
                self.stdout.write(f'  ... e mais {pratos_count - 3} pratos')
            self.stdout.write('')
        
        self.stdout.write('=== TODOS OS PRATOS ===')
        for prato in Prato.objects.all():
            self.stdout.write(f'{prato.nome} -> {prato.categoria.nome}')
