import os
import re
from django.core.management.base import BaseCommand
import pdfplumber


class Command(BaseCommand):
    help = 'Testa extração de descrições do PDF'

    def handle(self, *args, **options):
        # Buscar arquivo PDF
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        if not pdf_files:
            self.stdout.write(self.style.ERROR('Nenhum arquivo PDF encontrado'))
            return
        
        pdf_path = os.path.abspath(pdf_files[0])
        self.stdout.write(f'Testando PDF: {pdf_path}')
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Testar apenas as primeiras 5 páginas
                for page_num, page in enumerate(pdf.pages[:5], 1):
                    self.stdout.write(f'\n--- PÁGINA {page_num} ---')
                    
                    text = page.extract_text()
                    if not text:
                        self.stdout.write('Nenhum texto extraído')
                        continue
                    
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    self.stdout.write(f'Linhas encontradas: {len(lines)}')
                    
                    # Mostrar primeiras 20 linhas
                    for i, line in enumerate(lines[:20]):
                        self.stdout.write(f'{i+1:2d}: {line}')
                    
                    # Procurar por padrões de descrição
                    self.stdout.write('\n--- PADRÕES DE DESCRIÇÃO ---')
                    for i, line in enumerate(lines):
                        if self.eh_linha_descricao(line):
                            self.stdout.write(f'Linha {i+1}: {line}')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro: {str(e)}'))

    def eh_linha_descricao(self, line):
        """Verifica se uma linha parece ser uma descrição"""
        if len(line) < 15:
            return False
        
        # Não deve estar em maiúsculas (exceto primeira palavra)
        if line == line.upper() and len(line) > 20:
            return False
        
        # Deve ter características de descrição
        desc_words = [
            'com', 'de', 'em', 'para', 'molho', 'acompanhado',
            'servido', 'temperado', 'temperada', 'preparado', 'preparada',
            'feito', 'feita', 'cozido', 'cozida', 'grelhado', 'grelhada',
            'assado', 'assada', 'frito', 'frita', 'refogado', 'refogada',
            'delicioso', 'saboroso', 'cremoso', 'suave', 'picante'
        ]
        
        line_lower = line.lower()
        return any(word in line_lower for word in desc_words) or len(line) > 40

