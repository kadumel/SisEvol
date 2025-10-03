import os
import re
from django.core.management.base import BaseCommand
import pdfplumber


class Command(BaseCommand):
    help = 'Analisa categorias no PDF'

    def handle(self, *args, **options):
        # Buscar arquivo PDF
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        if not pdf_files:
            self.stdout.write(self.style.ERROR('Nenhum arquivo PDF encontrado'))
            return
        
        pdf_path = os.path.abspath(pdf_files[0])
        self.stdout.write(f'Analisando PDF: {pdf_path}')
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                self.stdout.write(f'Total de páginas: {total_pages}')
                
                categorias_encontradas = set()
                pratos_por_categoria = {}
                categoria_atual = None
                
                for page_num, page in enumerate(pdf.pages[:50], 1):  # Primeiras 50 páginas
                    if page_num % 10 == 0:
                        self.stdout.write(f'Processando página {page_num}')
                    
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    
                    for line in lines:
                        # Verificar se é cabeçalho de categoria
                        if self.eh_cabecalho_categoria(line):
                            categoria_atual = line.strip()
                            categorias_encontradas.add(categoria_atual)
                            if categoria_atual not in pratos_por_categoria:
                                pratos_por_categoria[categoria_atual] = []
                            self.stdout.write(f'  Categoria: {categoria_atual}')
                            continue
                        
                        # Verificar se é nome de prato
                        if self.eh_nome_prato(line):
                            prato_nome = line.strip()
                            if categoria_atual:
                                pratos_por_categoria[categoria_atual].append(prato_nome)
                                self.stdout.write(f'    Prato: {prato_nome}')
                
                self.stdout.write('\n=== RESUMO ===')
                self.stdout.write(f'Categorias encontradas: {len(categorias_encontradas)}')
                for cat in sorted(categorias_encontradas):
                    pratos_count = len(pratos_por_categoria.get(cat, []))
                    self.stdout.write(f'  {cat}: {pratos_count} pratos')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro: {str(e)}'))

    def eh_cabecalho_categoria(self, line):
        """Verifica se é cabeçalho de categoria"""
        if len(line) < 5:
            return False
        
        # Deve estar em maiúsculas
        if line != line.upper():
            return False
        
        # Palavras-chave de categoria
        keywords = [
            'ENTRADAS', 'PRATOS PRINCIPAIS', 'MASSAS', 'SOBREMESAS', 
            'BEBIDAS', 'APERITIVOS', 'ANTEPASTOS', 'CARNES', 'PEIXES',
            'SALADAS', 'SOPAS', 'DOCES', 'BEBIDAS QUENTES', 'BEBIDAS FRIAS'
        ]
        
        return any(keyword in line for keyword in keywords)

    def eh_nome_prato(self, line):
        """Verifica se é nome de prato"""
        if len(line) < 5:
            return False
        
        # Deve estar em maiúsculas
        if line != line.upper():
            return False
        
        # Não deve ser cabeçalho comum
        exclude = [
            'FICHA TÉCNICA', 'CARDÁPIO', 'CHEF', 'MENU', 'APRESENTAÇÃO',
            'SUMÁRIO', 'ÍNDICE', 'INTRODUÇÃO', 'INGREDIENTES', 'MODO',
            'PREPARO', 'MONTAGEM', 'UTENSÍLIOS', 'CALORIAS', 'TEMPO',
            'RENDIMENTO', 'DIFICULDADE', 'TEMPERATURA', 'DICAS',
            'CONSERVAÇÃO', 'VALOR NUTRICIONAL', 'ENTRADAS', 'PRATOS',
            'PRINCIPAIS', 'MASSAS', 'SOBREMESAS', 'BEBIDAS'
        ]
        
        if any(line.startswith(ex) for ex in exclude):
            return False
        
        # Deve ter pelo menos 5 caracteres alfabéticos
        letters = re.sub(r'[^A-Za-zÁÉÍÓÚÂÊÔÃÕÀÇáéíóúâêôãõàç]', '', line)
        return len(letters) >= 5
