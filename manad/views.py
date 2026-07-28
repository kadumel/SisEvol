from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from PerfilMenus.views import AcessoAcoes
from .models import (
    ImportacaoManad, ManadCabecalho, ManadEmpresa, ManadFuncionario,
    ManadLotacao, ManadEventoFolha, ManadDadosLaborais, ManadLancamentoFolha
)
from RH.models import Empresa, Funcionario, Cargo, Lotacao

class IndexManadView(LoginRequiredMixin, TemplateView):
    """View principal do módulo MANAD"""
    template_name = 'manad/index.html'

    def get(self, request, *args, **kwargs):
        acesso = AcessoAcoes(request, 'MANAD', 'Listar')
        if acesso == False:
            return render(request, 'Forbidden.html')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MANAD - Importação de Arquivos'
        context['total_importacoes'] = ImportacaoManad.objects.count()
        context['importacoes_recentes'] = ImportacaoManad.objects.all()[:5]
        return context


class ListImportacoesView(LoginRequiredMixin, ListView):
    """Lista todas as importações MANAD"""
    model = ImportacaoManad
    template_name = 'manad/list_importacoes.html'
    context_object_name = 'importacoes'
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        acesso = AcessoAcoes(request, 'MANAD', 'Listar')
        if acesso == False:
            return render(request, 'Forbidden.html')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Importações MANAD'
        return context


class ImportarManadView(LoginRequiredMixin, View):
    """View para importar arquivo MANAD"""
    template_name = 'manad/importar.html'
    
    def get(self, request):
        acesso = AcessoAcoes(request, 'MANAD', 'Inserir')
        if acesso == False:
            return render(request, 'Forbidden.html')

        context = {
            'title': 'Importar Arquivo MANAD'
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        acesso = AcessoAcoes(request, 'MANAD', 'Inserir')
        if acesso == False:
            return render(request, 'Forbidden.html')

        try:
            arquivo = request.FILES.get('arquivo')
            if not arquivo:
                messages.error(request, 'Por favor, selecione um arquivo para importar.')
                return render(request, self.template_name, {'title': 'Importar Arquivo MANAD'})
            
            # Criar registro de importação
            importacao = ImportacaoManad.objects.create(
                arquivo=arquivo.name,
                status='PROCESSANDO',
                usuario=request.user
            )
            
            # Processar data de referência se fornecida
            data_ref_str = request.POST.get('data_referencia')
            if data_ref_str:
                try:
                    # Formato MM/AAAA ou YYYY-MM
                    if '/' in data_ref_str:
                        mes, ano = data_ref_str.split('/')
                        importacao.data_referencia = datetime(int(ano), int(mes), 1).date()
                    else:
                        ano, mes = data_ref_str.split('-')
                        importacao.data_referencia = datetime(int(ano), int(mes), 1).date()
                except:
                    pass
            
            importacao.save()
            
            # Processar arquivo
            self.processar_arquivo(arquivo, importacao)
            
            messages.success(request, f'Importação iniciada! Total de registros: {importacao.total_registros}')
            return redirect('listImportacoesManad')
            
        except Exception as e:
            messages.error(request, f'Erro ao importar arquivo: {str(e)}')
            return render(request, self.template_name, {'title': 'Importar Arquivo MANAD'})
    
    def processar_arquivo(self, arquivo, importacao):
        """Processa o arquivo MANAD linha por linha"""
        try:
            conteudo = arquivo.read()
            if isinstance(conteudo, bytes):
                linhas = conteudo.decode('utf-8', errors='ignore').split('\n')
            else:
                linhas = conteudo.split('\n')
        except Exception as e:
            importacao.status = 'ERRO'
            importacao.observacoes = f'Erro ao ler arquivo: {str(e)}'
            importacao.save()
            return
        
        total_linhas = len([l for l in linhas if l.strip()])
        importacao.total_registros = total_linhas
        importacao.save()
        
        registros_processados = 0
        registros_erro = 0
        
        for num_linha, linha in enumerate(linhas, 1):
            linha = linha.strip()
            if not linha:
                continue
            
            try:
                # Separar campos por pipe
                campos = linha.split('|')
                if len(campos) < 1:
                    continue
                
                tipo_registro = campos[0].strip()
                
                # Processar cada tipo de registro
                if tipo_registro == '0000':
                    self.processar_registro_0000(campos, importacao)
                elif tipo_registro == '0100':
                    self.processar_registro_0100(campos, importacao)
                elif tipo_registro == 'K050':
                    self.processar_registro_K050(campos, importacao)
                elif tipo_registro == 'K100':
                    self.processar_registro_K100(campos, importacao)
                elif tipo_registro == 'K150':
                    self.processar_registro_K150(campos, importacao)
                elif tipo_registro == 'K250':
                    self.processar_registro_K250(campos, importacao)
                elif tipo_registro == 'K300':
                    self.processar_registro_K300(campos, importacao)
                else:
                    # Ignorar outros tipos de registro
                    continue
                
                registros_processados += 1
                
            except Exception as e:
                registros_erro += 1
                # Log do erro para debug
                if not importacao.observacoes:
                    importacao.observacoes = f'Erro na linha {num_linha}: {str(e)}\n'
                elif len(importacao.observacoes) < 900:
                    importacao.observacoes += f'Erro na linha {num_linha}: {str(e)}\n'
                continue
        
        # Atualizar status da importação
        importacao.registros_processados = registros_processados
        importacao.registros_erro = registros_erro
        importacao.status = 'CONCLUIDO' if registros_erro == 0 else 'CONCLUIDO'
        if registros_erro > 0:
            importacao.status = 'CONCLUIDO'  # Mesmo com erros, marca como concluído
        importacao.save()
    
    def parse_date(self, date_str):
        """Converte string de data DDMMAAAA para objeto date"""
        if not date_str or len(date_str) != 8:
            return None
        try:
            dia = int(date_str[:2])
            mes = int(date_str[2:4])
            ano = int(date_str[4:8])
            return datetime(ano, mes, dia).date()
        except:
            return None
    
    def parse_date_alt(self, date_str):
        """Converte string de data MMAAAA ou DDMMAAAA para objeto date"""
        if not date_str:
            return None
        date_str = date_str.strip()
        
        # Formato MMAAAA (6 caracteres)
        if len(date_str) == 6:
            try:
                mes = int(date_str[:2])
                ano = int(date_str[2:6])
                return datetime(ano, mes, 1).date()
            except:
                return None
        # Formato DDMMAAAA (8 caracteres)
        elif len(date_str) == 8:
            return self.parse_date(date_str)
        else:
            return None
    
    def get_campo(self, campos, indice, default=''):
        """Obtém campo do array com tratamento de índice"""
        try:
            if len(campos) > indice:
                valor = campos[indice].strip() if campos[indice] else ''
                return valor if valor else default
            return default
        except:
            return default
    
    def processar_registro_0000(self, campos, importacao):
        """Processa registro 0000 - Cabeçalho"""
        ManadCabecalho.objects.create(
            importacao=importacao,
            tipo_registro=self.get_campo(campos, 0, '0000'),
            nome=self.get_campo(campos, 1),
            cnpj=self.get_campo(campos, 2),
            cpf=self.get_campo(campos, 3),
            cei=self.get_campo(campos, 4),
            nit=self.get_campo(campos, 5),
            uf=self.get_campo(campos, 6),
            ie=self.get_campo(campos, 7),
            cod_mun=self.get_campo(campos, 8),
            im=self.get_campo(campos, 9),
            suframa=self.get_campo(campos, 10),
            ind_centr=self.get_campo(campos, 11),
            dt_ini=self.parse_date(self.get_campo(campos, 12)),
            dt_fin=self.parse_date(self.get_campo(campos, 13)),
            cod_ver=self.get_campo(campos, 14),
            cod_fin=self.get_campo(campos, 15),
            ind_ed=self.get_campo(campos, 16),
        )
    
    def processar_registro_0100(self, campos, importacao):
        """Processa registro 0100 - Empresa"""
        ManadEmpresa.objects.create(
            importacao=importacao,
            tipo_registro=self.get_campo(campos, 0, '0100'),
            emp_tec=self.get_campo(campos, 1),
            cargo=self.get_campo(campos, 2),
            dt_ini_serv_inf=self.parse_date(self.get_campo(campos, 3)),
            dt_fim_serv_inf=self.parse_date(self.get_campo(campos, 4)),
            cnpj=self.get_campo(campos, 5),
            cpf=self.get_campo(campos, 6),
            fone=self.get_campo(campos, 7),
            fax=self.get_campo(campos, 8),
            email=self.get_campo(campos, 9),
        )
    
    def processar_registro_K050(self, campos, importacao):
        """Processa registro K050 - Funcionário"""
        ManadFuncionario.objects.create(
            importacao=importacao,
            tipo_registro=self.get_campo(campos, 0, 'K050'),
            cnpj_cei=self.get_campo(campos, 1),
            dt_inc_alt=self.parse_date(self.get_campo(campos, 2)),
            cod_reg_trab=self.get_campo(campos, 3),
            cpf=self.get_campo(campos, 4),
            nit=self.get_campo(campos, 5),
            cod_categ=self.get_campo(campos, 6),
            nome_trab=self.get_campo(campos, 7),
            dt_nasc=self.parse_date(self.get_campo(campos, 8)),
            dt_admissao=self.parse_date(self.get_campo(campos, 9)),
            dt_demissao=self.parse_date(self.get_campo(campos, 10)),
            ind_vinc=self.get_campo(campos, 11),
            tipo_ato_nom=self.get_campo(campos, 12),
            nm_ato_nom=self.get_campo(campos, 13),
            dt_ato_nom=self.parse_date(self.get_campo(campos, 14)),
        )
    
    def processar_registro_K100(self, campos, importacao):
        """Processa registro K100 - Lotação"""
        ManadLotacao.objects.create(
            importacao=importacao,
            tipo_registro=self.get_campo(campos, 0, 'K100'),
            dt_inc_alt=self.parse_date_alt(self.get_campo(campos, 1)),
            cod_ltc=self.get_campo(campos, 2),
            cnpj_cei=self.get_campo(campos, 3),
            desc_ltc=self.get_campo(campos, 4),
            cnpj_cei_tom=self.get_campo(campos, 5),
        )
    
    def processar_registro_K150(self, campos, importacao):
        """Processa registro K150 - Evento Folha"""
        ManadEventoFolha.objects.create(
            importacao=importacao,
            tipo_registro=self.get_campo(campos, 0, 'K150'),
            cnpj_cei=self.get_campo(campos, 1),
            dt_inc_alt=self.parse_date_alt(self.get_campo(campos, 2)),
            cod_rubrica=self.get_campo(campos, 3),
            desc_rubrica=self.get_campo(campos, 4),
        )
    
    def processar_registro_K250(self, campos, importacao):
        """Processa registro K250 - Dados Laborais"""
        try:
            salario_base = float(self.get_campo(campos, 12).replace(',', '.')) if self.get_campo(campos, 12) else 0
            salario_compl = float(self.get_campo(campos, 13).replace(',', '.')) if self.get_campo(campos, 13) else 0
        except:
            salario_base = 0
            salario_compl = 0
        
        ManadDadosLaborais.objects.create(
            importacao=importacao,
            tipo_registro=self.get_campo(campos, 0, 'K250'),
            cnpj_cei=self.get_campo(campos, 1),
            ind_fl=self.get_campo(campos, 2),
            cod_ltc=self.get_campo(campos, 3),
            cod_reg_trab=self.get_campo(campos, 4),
            dt_comp=self.get_campo(campos, 5),
            dt_pgto=self.parse_date(self.get_campo(campos, 6)),
            cod_cbo=self.get_campo(campos, 7),
            cod_ocorr=self.get_campo(campos, 8),
            desc_cargo=self.get_campo(campos, 9),
            qtd_dep_ir=int(self.get_campo(campos, 10) or 0),
            qtd_dep_sf=int(self.get_campo(campos, 11) or 0),
            vl_base_irrf=salario_base,
            vl_base_ps=salario_compl,
        )
    
    def processar_registro_K300(self, campos, importacao):
        """Processa registro K300 - Lançamento Folha"""
        try:
            valor = float(self.get_campo(campos, 7).replace(',', '.')) if self.get_campo(campos, 7) else 0
        except:
            valor = 0
        
        ManadLancamentoFolha.objects.create(
            importacao=importacao,
            tipo_registro=self.get_campo(campos, 0, 'K300'),
            cnpj_cei=self.get_campo(campos, 1),
            ind_fl=self.get_campo(campos, 2),
            cod_ltc=self.get_campo(campos, 3),
            cod_reg_trab=self.get_campo(campos, 4),
            dt_comp=self.get_campo(campos, 5),
            cod_rubr=self.get_campo(campos, 6),
            vlr_rubr=valor,
            ind_rubr=self.get_campo(campos, 8),
            ind_base_irrf=self.get_campo(campos, 9),
            ind_base_ps=self.get_campo(campos, 10),
        )
