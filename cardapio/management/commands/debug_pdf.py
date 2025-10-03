import os
import sys
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Debug PDF'

    def handle(self, *args, **options):
        self.stdout.write('=== DEBUG PDF ===')
        self.stdout.write(f'Diretório atual: {os.getcwd()}')
        
        files = os.listdir('.')
        pdf_files = [f for f in files if f.endswith('.pdf')]
        self.stdout.write(f'Arquivos PDF: {pdf_files}')
        
        if pdf_files:
            pdf_path = pdf_files[0]
            self.stdout.write(f'Usando arquivo: {pdf_path}')
            self.stdout.write(f'Arquivo existe: {os.path.exists(pdf_path)}')
            
            try:
                import pdfplumber
                self.stdout.write('pdfplumber importado com sucesso')
                
                with pdfplumber.open(pdf_path) as pdf:
                    self.stdout.write(f'PDF aberto. Páginas: {len(pdf.pages)}')
                    
                    # Testar primeira página
                    page = pdf.pages[0]
                    text = page.extract_text()
                    if text:
                        self.stdout.write(f'Texto extraído (primeiros 200 chars): {text[:200]}')
                    else:
                        self.stdout.write('Nenhum texto extraído')
                        
            except Exception as e:
                self.stdout.write(f'Erro: {e}')
        else:
            self.stdout.write('Nenhum arquivo PDF encontrado')
