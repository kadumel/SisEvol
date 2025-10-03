import os
import re
from django.core.management.base import BaseCommand
from cardapio.models import Categoria, Prato
import pdfplumber


class Command(BaseCommand):
    help = 'Corrige categorias dos pratos baseado no PDF'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostra o que seria alterado sem fazer as mudanças'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Buscar arquivo PDF
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        if not pdf_files:
            self.stdout.write(self.style.ERROR('Nenhum arquivo PDF encontrado'))
            return
        
        pdf_path = os.path.abspath(pdf_files[0])
        self.stdout.write(f'Processando PDF: {pdf_path}')
        
        # Mapear categorias existentes
        categorias_map = {}
        for cat in Categoria.objects.all():
            categorias_map[cat.nome.lower()] = cat
            # Também mapear variações
            if 'entrada' in cat.nome.lower():
                categorias_map['entradas'] = cat
            elif 'principal' in cat.nome.lower():
                categorias_map['pratos principais'] = cat
            elif 'sobremesa' in cat.nome.lower():
                categorias_map['sobremesas'] = cat
            elif 'bebida' in cat.nome.lower():
                categorias_map['bebidas'] = cat
            elif 'massa' in cat.nome.lower():
                categorias_map['massas'] = cat
        
        self.stdout.write(f'Categorias mapeadas: {list(categorias_map.keys())}')
        
        # Palavras-chave para identificar categorias no PDF
        categoria_keywords = {
            'entradas': ['entrada', 'aperitivo', 'antepasto', 'petisco'],
            'pratos principais': ['prato principal', 'principal', 'carne', 'peixe', 'frango', 'bife', 'steak'],
            'massas': ['massa', 'pasta', 'espaguete', 'macarrão', 'ravioli', 'lasanha'],
            'sobremesas': ['sobremesa', 'doce', 'pudim', 'torta', 'sorvete', 'mousse'],
            'bebidas': ['bebida', 'suco', 'refrigerante', 'água', 'café', 'chá']
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                self.stdout.write(f'Total de páginas: {total_pages}')
                
                pratos_atualizados = 0
                categoria_atual = None
                
                for page_num, page in enumerate(pdf.pages, 1):
                    if page_num % 20 == 0:
                        self.stdout.write(f'Processando página {page_num}/{total_pages}')
                    
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    
                    for line in lines:
                        # Verificar se é um cabeçalho de categoria
                        categoria_detectada = self.detectar_categoria(line, categoria_keywords)
                        if categoria_detectada:
                            categoria_atual = categoria_detectada
                            self.stdout.write(f'  Categoria detectada: {categoria_atual}')
                            continue
                        
                        # Verificar se é um nome de prato (linha em maiúsculas)
                        if self.eh_nome_prato(line):
                            prato_nome = line.strip()
                            
                            # Buscar prato no banco
                            try:
                                prato = Prato.objects.get(nome__iexact=prato_nome)
                                
                                # Determinar categoria correta
                                categoria_correta = self.determinar_categoria(prato_nome, categoria_atual, categorias_map, categoria_keywords)
                                
                                if categoria_correta and prato.categoria != categoria_correta:
                                    if dry_run:
                                        self.stdout.write(f'  [DRY-RUN] {prato.nome}: {prato.categoria.nome} -> {categoria_correta.nome}')
                                    else:
                                        prato.categoria = categoria_correta
                                        prato.save()
                                        self.stdout.write(f'  Atualizado: {prato.nome} -> {categoria_correta.nome}')
                                    pratos_atualizados += 1
                                    
                            except Prato.DoesNotExist:
                                self.stdout.write(f'  Prato não encontrado: {prato_nome}')
                            except Prato.MultipleObjectsReturned:
                                self.stdout.write(f'  Múltiplos pratos encontrados: {prato_nome}')
                
                if dry_run:
                    self.stdout.write(self.style.WARNING(f'[DRY-RUN] {pratos_atualizados} pratos seriam atualizados'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'{pratos_atualizados} pratos atualizados'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro: {str(e)}'))

    def detectar_categoria(self, line, categoria_keywords):
        """Detecta se uma linha é um cabeçalho de categoria"""
        line_lower = line.lower()
        
        # Padrões para cabeçalhos de categoria
        patterns = [
            r'^[A-Z\s]+ENTRADAS?[A-Z\s]*$',
            r'^[A-Z\s]+PRATOS?\s+PRINCIPAIS?[A-Z\s]*$',
            r'^[A-Z\s]+MASSAS?[A-Z\s]*$',
            r'^[A-Z\s]+SOBREMESAS?[A-Z\s]*$',
            r'^[A-Z\s]+BEBIDAS?[A-Z\s]*$',
        ]
        
        for pattern in patterns:
            if re.match(pattern, line, re.IGNORECASE):
                # Extrair tipo de categoria
                for tipo, keywords in categoria_keywords.items():
                    if any(keyword in line_lower for keyword in keywords):
                        return tipo
        
        return None

    def eh_nome_prato(self, line):
        """Verifica se uma linha é um nome de prato"""
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
            'CONSERVAÇÃO', 'VALOR NUTRICIONAL'
        ]
        
        if any(line.startswith(ex) for ex in exclude):
            return False
        
        # Deve ter pelo menos 5 caracteres alfabéticos
        letters = re.sub(r'[^A-Za-zÁÉÍÓÚÂÊÔÃÕÀÇáéíóúâêôãõàç]', '', line)
        return len(letters) >= 5

    def determinar_categoria(self, prato_nome, categoria_atual, categorias_map, categoria_keywords):
        """Determina a categoria correta para um prato"""
        prato_lower = prato_nome.lower()
        
        # 1. Usar categoria detectada no contexto
        if categoria_atual and categoria_atual in categorias_map:
            return categorias_map[categoria_atual]
        
        # 2. Buscar por palavras-chave no nome do prato
        for tipo, keywords in categoria_keywords.items():
            if any(keyword in prato_lower for keyword in keywords):
                if tipo in categorias_map:
                    return categorias_map[tipo]
        
        # 3. Buscar categoria mais próxima por nome
        for cat_nome, categoria in categorias_map.items():
            if any(palavra in prato_lower for palavra in cat_nome.split()):
                return categoria
        
        return None
