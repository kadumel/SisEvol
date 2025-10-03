from django.core.management.base import BaseCommand
from cardapio.models import Prato


class Command(BaseCommand):
    help = 'Atualiza descrições dos pratos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostra o que seria alterado sem fazer as mudanças'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Mapeamento manual de descrições baseado no PDF
        descricoes_map = {
            'STEAK DE MAMINHA': 'Corte nobre de carne bovina grelhado ao ponto desejado, acompanhado de molho especial e guarnições.',
            'MAMINHA CURADA': 'Carne bovina curada e temperada, grelhada e servida com acompanhamentos especiais.',
            'COXA E SOBRECOXA CASQUEIRADA': 'Cortes de frango temperados e grelhados, servidos com molho e guarnições.',
            'CHORIZO SUÍNO': 'Embutido suíno temperado e grelhado, servido com acompanhamentos tradicionais.',
            'SALMÃO ASIÁTICO': 'Filé de salmão grelhado com temperos asiáticos, acompanhado de molho especial.',
            'SALADA DE FRUTOS DO MAR': 'Mistura de frutos do mar frescos servidos sobre folhas verdes com molho especial.',
            'SALADA SMOKED CAESAR': 'Salada Caesar tradicional com alface romana, croutons e molho Caesar, enriquecida com elementos defumados.',
            'MENU EXECUTIVO': 'Refeição completa com entrada, prato principal e sobremesa, ideal para o almoço executivo.',
            'MENU': 'Opção completa de refeição com entrada, prato principal e acompanhamentos.',
            'RISOTTO DE CAMARÃO': 'Arroz cremoso preparado com camarões frescos e temperos especiais.',
            'LAGOSTA THERMIDOR': 'Lagosta preparada com molho termidor, gratinada e servida com acompanhamentos.',
            'FILÉ MIGNON': 'Corte nobre de carne bovina grelhado ao ponto desejado, servido com molho especial.',
            'PEIXE DO DIA': 'Peixe fresco do dia preparado conforme disponibilidade, grelhado ou assado.',
            'FRANGO GRELHADO': 'Peito de frango temperado e grelhado, servido com molho e acompanhamentos.',
            'SALMÃO GRELHADO': 'Filé de salmão fresco grelhado com temperos especiais e molho.',
            'LAGOSTA GRELHADA': 'Lagosta fresca grelhada e servida com manteiga temperada e acompanhamentos.',
            'SALADA VERDE': 'Mistura de folhas verdes frescas com tomate cereja e molho especial.',
            'SALADA DE QUINOA': 'Salada nutritiva com quinoa, vegetais frescos e molho especial.',
            'SOPA DO DIA': 'Sopa preparada diariamente com ingredientes frescos e sazonais.',
            'SOPA DE LEGUMES': 'Sopa cremosa de legumes frescos temperada com ervas especiais.',
            'SORVETE ARTESANAL': 'Sorvete feito na casa com sabores especiais e ingredientes selecionados.',
            'TIRAMISU': 'Sobremesa italiana tradicional com café, mascarpone e cacau em pó.',
            'PUDIM DE LEITE': 'Pudim cremoso de leite condensado com calda de caramelo.',
            'CAFÉ ESPECIAL': 'Café selecionado preparado com técnicas especiais para realçar o sabor.',
            'SUCO NATURAL': 'Suco fresco preparado na hora com frutas selecionadas.',
        }
        
        pratos_sem_descricao = Prato.objects.filter(
            descricao__isnull=True
        ).exclude(descricao__gt='')
        
        self.stdout.write(f'Pratos sem descrição: {pratos_sem_descricao.count()}')
        
        pratos_atualizados = 0
        
        for prato in pratos_sem_descricao:
            # Buscar descrição no mapeamento
            descricao = None
            
            # Tentar correspondência exata
            if prato.nome.upper() in descricoes_map:
                descricao = descricoes_map[prato.nome.upper()]
            else:
                # Tentar correspondência parcial
                for nome_map, desc in descricoes_map.items():
                    if nome_map in prato.nome.upper() or prato.nome.upper() in nome_map:
                        descricao = desc
                        break
            
            if descricao:
                if dry_run:
                    self.stdout.write(f'[DRY-RUN] {prato.nome}: "{descricao[:50]}..."')
                else:
                    prato.descricao = descricao
                    prato.save()
                    self.stdout.write(f'Atualizado: {prato.nome}')
                pratos_atualizados += 1
            else:
                self.stdout.write(f'Sem descrição encontrada: {prato.nome}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING(f'[DRY-RUN] {pratos_atualizados} pratos seriam atualizados'))
        else:
            self.stdout.write(self.style.SUCCESS(f'{pratos_atualizados} pratos atualizados'))

