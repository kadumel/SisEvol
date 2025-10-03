import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from cardapio.models import Categoria, Prato
import pdfplumber


class Command(BaseCommand):
    help = 'Importa dados de fichas técnicas de um arquivo PDF'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pdf-path',
            type=str,
            default='Ficha Técnica.pdf',
            help='Caminho para o arquivo PDF (padrão: Ficha Técnica.pdf)'
        )
        parser.add_argument(
            '--criar-categorias',
            action='store_true',
            help='Cria categorias automaticamente se não existirem'
        )

    def handle(self, *args, **options):
        # Buscar arquivo PDF automaticamente
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        if not pdf_files:
            self.stdout.write(
                self.style.ERROR('Nenhum arquivo PDF encontrado no diretório atual')
            )
            return
        
        pdf_path = os.path.abspath(pdf_files[0])
        criar_categorias = options['criar_categorias']
        
        self.stdout.write(f'Usando arquivo PDF: {pdf_path}')

        self.stdout.write(f'Processando arquivo: {pdf_path}')
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                self.stdout.write(f'Total de páginas: {total_pages}')
                
                pratos_importados = 0
                
                # Processar todas as páginas
                for page_num, page in enumerate(pdf.pages, 1):
                    if page_num % 10 == 0:  # Mostrar progresso a cada 10 páginas
                        self.stdout.write(f'Processando página {page_num}/{total_pages}')
                    
                    # Extrair texto da página
                    text = page.extract_text()
                    if not text:
                        self.stdout.write(f'  Nenhum texto na página {page_num}')
                        continue
                    
                    self.stdout.write(f'  Texto extraído: {len(text)} caracteres')
                    
                    # Processar pratos da página
                    pratos = self.extrair_pratos_da_pagina(text, page_num)
                    self.stdout.write(f'  Pratos encontrados: {len(pratos)}')
                    
                    for prato_data in pratos:
                        if self.importar_prato(prato_data, criar_categorias):
                            pratos_importados += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Importação concluída! {pratos_importados} pratos importados.'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao processar PDF: {str(e)}')
            )

    def extrair_pratos_da_pagina(self, text, page_num):
        """Extrai dados de pratos de uma página do PDF"""
        pratos = []
        
        # Dividir o texto em seções (assumindo que cada prato é uma seção)
        # Este é um exemplo básico - pode precisar ser ajustado conforme o formato do PDF
        sections = self.dividir_em_secoes(text)
        
        for section in sections:
            prato_data = self.extrair_dados_do_prato(section, page_num)
            if prato_data:
                pratos.append(prato_data)

        # Fallback: se nada foi detectado, tenta tratar a página como um único prato
        if not pratos:
            fallback = self.extrair_dados_do_prato(text, page_num, force_single=True)
            if fallback:
                pratos.append(fallback)

        return pratos

    def dividir_em_secoes(self, text):
        """Divide o texto em seções de pratos"""
        # Padrões para identificar início de pratos
        patterns = [
            r'PRATO:\s*(.+?)(?=PRATO:|$)',  # PRATO: nome do prato
            r'FICHA TÉCNICA:\s*(.+?)(?=FICHA TÉCNICA:|$)',  # FICHA TÉCNICA: nome
            r'^(.+?)(?=\n\n|\n[A-ZÁÊÇÕ][A-ZÁÊÇÕ\s]+:|\n\d+\.|\n•)',  # Nome do prato seguido de detalhes
        ]
        
        sections = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
            for match in matches:
                section = match.group(1).strip()
                if len(section) > 50:  # Filtrar seções muito pequenas
                    sections.append(section)
        
        # Se não encontrou padrões específicos, dividir por quebras de linha duplas
        if not sections:
            sections = [s.strip() for s in text.split('\n\n') if len(s.strip()) > 50]
        
        return sections

    def extrair_dados_do_prato(self, section, page_num, force_single=False):
        """Extrai dados estruturados de uma seção de prato"""
        lines = [ln.strip() for ln in section.split('\n') if ln.strip()]
        prato_data = {
            'nome': '',
            'categoria': 'Geral',  # Categoria padrão
            'descricao': '',
            'ingredientes': [],
            'quantitativo_ingredientes': [],
            'modo_preparo': [],
            'montagem_prato': [],
            'utensilios_necessarios': [],
            'calorias': 0,
            'tempo_preparo': 0,
            'rendimento': '',
            'dificuldade': 'medio',
            'temperatura_servico': '',
            'dicas_chef': '',
            'conservacao': '',
            'valor_nutricional': '',
            'imagem': '',
            'page_num': page_num
        }
        
        # Extrair nome do prato
        # 1) Tentar primeira linha totalmente em maiúsculas plausível
        upper_exclude = (
            'FICHA TÉCNICA', 'CARDÁPIO', 'CHEF', 'MENU', 'APRESENTAÇÃO',
            'SUMÁRIO', 'ÍNDICE', 'INTRODUÇÃO'
        )
        for line in lines[:10]:
            only_letters = re.sub(r'[^A-Za-zÁÉÍÓÚÂÊÔÃÕÀÇáéíóúâêôãõàç ]', '', line)
            if (
                len(only_letters.strip()) >= 5 and
                line == line.upper() and
                not any(line.startswith(ex) for ex in upper_exclude)
            ):
                prato_data['nome'] = line.strip()
                break
        # 2) Fallback: primeira linha significativa que não é cabeçalho
        if not prato_data['nome']:
            for line in lines[:10]:
                if not re.match(r'^(INGREDIENTES|QUANTITATIVO|MODO|MONTAGEM|UTENSÍLIOS|CALORIAS|TEMPO|RENDIMENTO|DIFICULDADE|TEMPERATURA|DICAS|CONSERVAÇÃO|VALOR)', line, re.IGNORECASE):
                    if len(line) > 3:
                        prato_data['nome'] = line.strip()
                        break
        
        # Processar cada linha para extrair informações
        current_section = None
        for line in lines:
            if not line:
                continue
                
            # Identificar seções
            if re.match(r'INGREDIENTES?', line, re.IGNORECASE):
                current_section = 'ingredientes'
                continue
            elif re.match(r'QUANTITATIVO', line, re.IGNORECASE):
                current_section = 'quantitativo'
                continue
            elif re.match(r'MODO\s+DE\s+PREPARO', line, re.IGNORECASE):
                current_section = 'preparo'
                continue
            elif re.match(r'MONTAGEM', line, re.IGNORECASE):
                current_section = 'montagem'
                continue
            elif re.match(r'UTENSÍLIOS?', line, re.IGNORECASE):
                current_section = 'utensilios'
                continue
            elif re.match(r'CALORIAS?', line, re.IGNORECASE):
                current_section = 'calorias'
                continue
            elif re.match(r'TEMPO', line, re.IGNORECASE):
                current_section = 'tempo'
                continue
            elif re.match(r'RENDIMENTO', line, re.IGNORECASE):
                current_section = 'rendimento'
                continue
            elif re.match(r'DIFICULDADE', line, re.IGNORECASE):
                current_section = 'dificuldade'
                continue
            elif re.match(r'TEMPERATURA', line, re.IGNORECASE):
                current_section = 'temperatura'
                continue
            elif re.match(r'DICAS?', line, re.IGNORECASE):
                current_section = 'dicas'
                continue
            elif re.match(r'CONSERVAÇÃO', line, re.IGNORECASE):
                current_section = 'conservacao'
                continue
            elif re.match(r'VALOR\s+NUTRICIONAL', line, re.IGNORECASE):
                current_section = 'nutricional'
                continue
            
            # Processar conteúdo baseado na seção atual
            if current_section == 'ingredientes':
                if line.startswith(('•', '-', '*', '◦')):
                    prato_data['ingredientes'].append(line[1:].strip())
                elif not line.startswith(('INGREDIENTES', 'QUANTITATIVO', 'MODO', 'PREPARO')):
                    prato_data['ingredientes'].append(line)
            
            elif current_section == 'quantitativo':
                if line.startswith(('•', '-', '*', '◦')):
                    prato_data['quantitativo_ingredientes'].append(line[1:].strip())
                elif not line.startswith(('QUANTITATIVO', 'MODO', 'PREPARO', 'MONTAGEM')):
                    prato_data['quantitativo_ingredientes'].append(line)
            
            elif current_section == 'preparo':
                if line.startswith(('•', '-', '*', '◦', '1.', '2.', '3.', '4.', '5.')):
                    prato_data['modo_preparo'].append(line)
                elif not line.startswith(('MODO', 'PREPARO', 'MONTAGEM', 'UTENSÍLIOS')):
                    prato_data['modo_preparo'].append(line)
            
            elif current_section == 'montagem':
                if line.startswith(('•', '-', '*', '◦')):
                    prato_data['montagem_prato'].append(line[1:].strip())
                elif not line.startswith(('MONTAGEM', 'UTENSÍLIOS', 'CALORIAS')):
                    prato_data['montagem_prato'].append(line)
            
            elif current_section == 'utensilios':
                if line.startswith(('•', '-', '*', '◦')):
                    prato_data['utensilios_necessarios'].append(line[1:].strip())
                elif not line.startswith(('UTENSÍLIOS', 'CALORIAS', 'TEMPO')):
                    prato_data['utensilios_necessarios'].append(line)
            
            elif current_section == 'calorias':
                calorias = re.search(r'(\d+)', line)
                if calorias:
                    prato_data['calorias'] = int(calorias.group(1))
            
            elif current_section == 'tempo':
                tempo = re.search(r'(\d+)', line)
                if tempo:
                    prato_data['tempo_preparo'] = int(tempo.group(1))
            
            elif current_section == 'rendimento':
                prato_data['rendimento'] = line
            
            elif current_section == 'dificuldade':
                if 'fácil' in line.lower():
                    prato_data['dificuldade'] = 'facil'
                elif 'difícil' in line.lower():
                    prato_data['dificuldade'] = 'dificil'
                else:
                    prato_data['dificuldade'] = 'medio'
            
            elif current_section == 'temperatura':
                prato_data['temperatura_servico'] = line
            
            elif current_section == 'dicas':
                prato_data['dicas_chef'] += line + ' '
            
            elif current_section == 'conservacao':
                prato_data['conservacao'] += line + ' '
            
            elif current_section == 'nutricional':
                prato_data['valor_nutricional'] += line + ' '
        
        # Limpar dados
        prato_data['dicas_chef'] = prato_data['dicas_chef'].strip()
        prato_data['conservacao'] = prato_data['conservacao'].strip()
        prato_data['valor_nutricional'] = prato_data['valor_nutricional'].strip()
        
        # Filtrar listas vazias
        for key in ['ingredientes', 'quantitativo_ingredientes', 'modo_preparo', 
                   'montagem_prato', 'utensilios_necessarios']:
            prato_data[key] = [item for item in prato_data[key] if item.strip()]
        
        # Se for fallback e ainda não há nome, não retornar
        if not prato_data['nome'] and force_single:
            return None
        # Só retornar se tem nome
        if prato_data['nome']:
            return prato_data
        
        return None

    def importar_prato(self, prato_data, criar_categorias):
        """Importa um prato para o banco de dados"""
        try:
            # Buscar ou criar categoria
            categoria, created = Categoria.objects.get_or_create(
                nome=prato_data['categoria'],
                defaults={
                    'descricao': f'Categoria importada do PDF',
                    'icone': 'bi-grid-3x3-gap',
                    'cor': '#667eea',
                    'ativo': True,
                    'ordem': 999
                }
            )
            
            if created and criar_categorias:
                self.stdout.write(f'Criada categoria: {categoria.nome}')
            
            # Criar prato
            prato, created = Prato.objects.get_or_create(
                nome=prato_data['nome'],
                categoria=categoria,
                defaults={
                    'descricao': prato_data['descricao'],
                    'ingredientes': '\n'.join(prato_data['ingredientes']),
                    'quantitativo_ingredientes': '\n'.join(prato_data['quantitativo_ingredientes']),
                    'modo_preparo': '\n'.join(prato_data['modo_preparo']),
                    'montagem_prato': '\n'.join(prato_data['montagem_prato']),
                    'utensilios_necessarios': '\n'.join(prato_data['utensilios_necessarios']),
                    'calorias': prato_data['calorias'],
                    'tempo_preparo': prato_data['tempo_preparo'],
                    'rendimento': prato_data['rendimento'],
                    'dificuldade': prato_data['dificuldade'],
                    'temperatura_servico': prato_data['temperatura_servico'],
                    'dicas_chef': prato_data['dicas_chef'],
                    'conservacao': prato_data['conservacao'],
                    'valor_nutricional': prato_data['valor_nutricional'],
                    'imagem': prato_data['imagem'],
                    'preco': 0.00,  # Preço padrão para pratos importados
                    'ativo': True,
                    'vegetariano': False,
                    'vegano': False,
                    'sem_gluten': False,
                    'sem_lactose': False
                }
            )
            
            if created:
                self.stdout.write(f'Criado prato: {prato.nome}')
                return True
            else:
                # Atualiza campos quando vierem preenchidos
                fields_to_update = [
                    ('descricao', prato_data['descricao']),
                    ('ingredientes', '\n'.join(prato_data['ingredientes'])),
                    ('quantitativo_ingredientes', '\n'.join(prato_data['quantitativo_ingredientes'])),
                    ('modo_preparo', '\n'.join(prato_data['modo_preparo'])),
                    ('montagem_prato', '\n'.join(prato_data['montagem_prato'])),
                    ('utensilios_necessarios', '\n'.join(prato_data['utensilios_necessarios'])),
                    ('calorias', prato_data['calorias']),
                    ('tempo_preparo', prato_data['tempo_preparo']),
                    ('rendimento', prato_data['rendimento']),
                    ('dificuldade', prato_data['dificuldade']),
                    ('temperatura_servico', prato_data['temperatura_servico']),
                ]
                changed = False
                for field, value in fields_to_update:
                    if value:
                        setattr(prato, field, value)
                        changed = True
                if changed:
                    prato.save()
                    self.stdout.write(f'Prato atualizado: {prato.nome}')
                else:
                    self.stdout.write(f'Prato já existe: {prato.nome}')
                return False
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao importar prato {prato_data.get("nome", "desconhecido")}: {str(e)}')
            )
            return False
