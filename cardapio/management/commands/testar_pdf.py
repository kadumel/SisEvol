import os
from django.core.management.base import BaseCommand
import pdfplumber


class Command(BaseCommand):
    help = 'Testa extração de texto do PDF'

    def handle(self, *args, **options):
        # Buscar arquivo PDF
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        if not pdf_files:
            self.stdout.write(self.style.ERROR('Nenhum arquivo PDF encontrado'))
            return
        pdf_path = os.path.abspath(pdf_files[0])
        
        self.stdout.write(f'Verificando arquivo: {pdf_path}')
        self.stdout.write(f'Arquivo existe: {os.path.exists(pdf_path)}')
        
        if not os.path.exists(pdf_path):
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado: {pdf_path}'))
            return
        
        self.stdout.write(f'Processando: {pdf_path}')
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                self.stdout.write(f'Total de páginas: {len(pdf.pages)}')
                
                for i, page in enumerate(pdf.pages[:3]):  # Apenas as 3 primeiras páginas
                    self.stdout.write(f'\n--- PÁGINA {i+1} ---')
                    text = page.extract_text()
                    if text:
                        # Mostrar apenas as primeiras 500 caracteres
                        self.stdout.write(text[:500] + '...' if len(text) > 500 else text)
                    else:
                        self.stdout.write('Nenhum texto extraído desta página')
                        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro: {str(e)}'))
