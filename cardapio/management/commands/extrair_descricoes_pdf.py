import os
import re
from django.core.management.base import BaseCommand
from cardapio.models import Prato
import pdfplumber


class Command(BaseCommand):
    help = 'Extrai e insere descrições dos pratos do PDF'

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
        
        # Obter todos os pratos existentes
        pratos_existentes = {prato.nome.lower(): prato for prato in Prato.objects.all()}
        self.stdout.write(f'Pratos existentes: {len(pratos_existentes)}')
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                self.stdout.write(f'Total de páginas: {total_pages}')
                
                pratos_atualizados = 0
                
                for page_num, page in enumerate(pdf.pages, 1):
                    if page_num % 20 == 0:
                        self.stdout.write(f'Processando página {page_num}/{total_pages}')
                    
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    # Processar pratos da página
                    pratos_encontrados = self.extrair_pratos_com_descricao(text, page_num)
                    
                    for prato_data in pratos_encontrados:
                        nome_prato = prato_data['nome']
                        descricao = prato_data['descricao']
                        
                        # Buscar prato no banco
                        prato_encontrado = None
                        for nome_lower, prato in pratos_existentes.items():
                            if nome_prato.lower() in nome_lower or nome_lower in nome_prato.lower():
                                prato_encontrado = prato
                                break
                        
                        if prato_encontrado and descricao and len(descricao.strip()) > 10:
                            if not prato_encontrado.descricao or len(prato_encontrado.descricao.strip()) < 10:
                                if dry_run:
                                    self.stdout.write(f'  [DRY-RUN] {prato_encontrado.nome}: "{descricao[:50]}..."')
                                else:
                                    prato_encontrado.descricao = descricao.strip()
                                    prato_encontrado.save()
                                    self.stdout.write(f'  Atualizado: {prato_encontrado.nome}')
                                pratos_atualizados += 1
                
                if dry_run:
                    self.stdout.write(self.style.WARNING(f'[DRY-RUN] {pratos_atualizados} pratos seriam atualizados'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'{pratos_atualizados} pratos atualizados'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro: {str(e)}'))

    def extrair_pratos_com_descricao(self, text, page_num):
        """Extrai pratos com suas descrições do texto"""
        pratos = []
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Verificar se é nome de prato
            if self.eh_nome_prato(line):
                prato_nome = line.strip()
                
                # Procurar descrição nas próximas linhas
                descricao = self.extrair_descricao_do_prato(lines, i + 1)
                
                if descricao:
                    pratos.append({
                        'nome': prato_nome,
                        'descricao': descricao,
                        'page_num': page_num
                    })
            
            i += 1
        
        return pratos

    def extrair_descricao_do_prato(self, lines, start_index):
        """Extrai descrição de um prato a partir de uma posição"""
        descricao_parts = []
        
        for i in range(start_index, min(start_index + 10, len(lines))):
            line = lines[i]
            
            # Parar se encontrar outro prato ou seção
            if self.eh_nome_prato(line) or self.eh_cabecalho_secao(line):
                break
            
            # Parar se encontrar ingredientes ou modo de preparo
            if re.match(r'^(INGREDIENTES|QUANTITATIVO|MODO|PREPARO|MONTAGEM)', line, re.IGNORECASE):
                break
            
            # Adicionar linha se parecer com descrição
            if self.eh_linha_descricao(line):
                descricao_parts.append(line)
        
        return ' '.join(descricao_parts).strip()

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

    def eh_cabecalho_secao(self, line):
        """Verifica se é cabeçalho de seção"""
        return re.match(r'^(ENTRADAS|PRATOS|MASSAS|SOBREMESAS|BEBIDAS)', line, re.IGNORECASE)

    def eh_linha_descricao(self, line):
        """Verifica se uma linha parece ser uma descrição"""
        if len(line) < 10:
            return False
        
        # Não deve estar em maiúsculas (exceto primeira palavra)
        if line == line.upper() and len(line) > 20:
            return False
        
        # Deve ter características de descrição
        # - Contém palavras comuns de descrição
        desc_words = [
            'com', 'de', 'em', 'para', 'com', 'molho', 'acompanhado',
            'servido', 'temperado', 'temperada', 'preparado', 'preparada',
            'feito', 'feita', 'cozido', 'cozida', 'grelhado', 'grelhada',
            'assado', 'assada', 'frito', 'frita', 'refogado', 'refogada'
        ]
        
        line_lower = line.lower()
        return any(word in line_lower for word in desc_words) or len(line) > 30

