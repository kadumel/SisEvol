from django.db import models
from django.contrib.auth.models import User
from RH.models import Empresa, Funcionario, Cargo, Lotacao

# ============================================================================
# MODELOS PARA IMPORTAÇÃO DO ARQUIVO MANAD
# Baseado no Manual Normativo de Arquivos Digitais - MANAD
# Versão 1.0.0.2
# ============================================================================

class ImportacaoManad(models.Model):
    """Modelo para controlar as importações de arquivos MANAD"""
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('PROCESSANDO', 'Processando'),
        ('CONCLUIDO', 'Concluído'),
        ('ERRO', 'Erro'),
    )
    
    arquivo = models.CharField('Nome do Arquivo', max_length=255)
    data_importacao = models.DateTimeField('Data de Importação', auto_now_add=True)
    data_referencia = models.DateField('Data de Referência', null=True, blank=True)
    total_registros = models.IntegerField('Total de Registros', default=0)
    registros_processados = models.IntegerField('Registros Processados', default=0)
    registros_erro = models.IntegerField('Registros com Erro', default=0)
    status = models.CharField('Status', max_length=20, default='PENDENTE', choices=STATUS_CHOICES)
    observacoes = models.TextField('Observações', max_length=1000, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-data_importacao']
        verbose_name = 'Importação MANAD'
        verbose_name_plural = 'Importações MANAD'
    
    def __str__(self):
        return f"{self.arquivo} - {self.data_importacao.strftime('%d/%m/%Y %H:%M')}"


class ManadCabecalho(models.Model):
    """Registro 0000 - Abertura do arquivo digital e identificação dos estabelecimentos"""
    importacao = models.ForeignKey(ImportacaoManad, on_delete=models.CASCADE, related_name='cabecalhos')
    tipo_registro = models.CharField('Tipo Registro', max_length=4, default='0000')
    nome = models.CharField('Nome Empresarial', max_length=255, null=True, blank=True)
    cnpj = models.CharField('CNPJ', max_length=14, null=True, blank=True)
    cpf = models.CharField('CPF', max_length=11, null=True, blank=True)
    cei = models.CharField('CEI', max_length=12, null=True, blank=True)
    nit = models.CharField('NIT', max_length=11, null=True, blank=True)
    uf = models.CharField('UF', max_length=2, null=True, blank=True)
    ie = models.CharField('Inscrição Estadual', max_length=20, null=True, blank=True)
    cod_mun = models.CharField('Código Município', max_length=7, null=True, blank=True)
    im = models.CharField('Inscrição Municipal', max_length=20, null=True, blank=True)
    suframa = models.CharField('SUFRAMA', max_length=9, null=True, blank=True)
    ind_centr = models.CharField('Indicador Centralização', max_length=1, null=True, blank=True)
    dt_ini = models.DateField('Data Início', null=True, blank=True)
    dt_fin = models.DateField('Data Fim', null=True, blank=True)
    cod_ver = models.CharField('Código Versão', max_length=3, null=True, blank=True)
    cod_fin = models.CharField('Código Finalidade', max_length=2, null=True, blank=True)
    ind_ed = models.CharField('Indicador Entrada Dados', max_length=1, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Cabeçalho MANAD'
        verbose_name_plural = 'Cabeçalhos MANAD'
    
    def __str__(self):
        return f"Cabeçalho - {self.cnpj or self.cpf}"


class ManadEmpresa(models.Model):
    """Registro 0100 - Dados do técnico/empresa responsável pela geração do arquivo digital"""
    importacao = models.ForeignKey(ImportacaoManad, on_delete=models.CASCADE, related_name='empresas')
    tipo_registro = models.CharField('Tipo Registro', max_length=4, default='0100')
    emp_tec = models.CharField('Empresa/Técnico', max_length=255, null=True, blank=True)
    cargo = models.CharField('Cargo', max_length=100, null=True, blank=True)
    dt_ini_serv_inf = models.DateField('Data Início Serviço Informática', null=True, blank=True)
    dt_fim_serv_inf = models.DateField('Data Fim Serviço Informática', null=True, blank=True)
    cnpj = models.CharField('CNPJ', max_length=14, null=True, blank=True)
    cpf = models.CharField('CPF', max_length=11, null=True, blank=True)
    fone = models.CharField('Telefone', max_length=20, null=True, blank=True)
    fax = models.CharField('Fax', max_length=20, null=True, blank=True)
    email = models.CharField('E-mail', max_length=255, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Empresa MANAD'
        verbose_name_plural = 'Empresas MANAD'
    
    def __str__(self):
        return f"{self.emp_tec} - {self.cnpj or self.cpf}"


class ManadFuncionario(models.Model):
    """Registro K050 - Cadastro de trabalhadores"""
    importacao = models.ForeignKey(ImportacaoManad, on_delete=models.CASCADE, related_name='funcionarios')
    tipo_registro = models.CharField('Tipo Registro', max_length=4, default='K050')
    cnpj_cei = models.CharField('CNPJ/CEI', max_length=14, null=True, blank=True)
    dt_inc_alt = models.DateField('Data Inclusão/Alteração', null=True, blank=True)
    cod_reg_trab = models.CharField('Código Registro Trabalhador', max_length=20, null=True, blank=True)
    cpf = models.CharField('CPF', max_length=11, null=True, blank=True)
    nit = models.CharField('NIT (PIS/PASEP/SUS)', max_length=11, null=True, blank=True)
    cod_categ = models.CharField('Código Categoria', max_length=2, null=True, blank=True)
    nome_trab = models.CharField('Nome Trabalhador', max_length=255, null=True, blank=True)
    dt_nasc = models.DateField('Data Nascimento', null=True, blank=True)
    dt_admissao = models.DateField('Data Admissão', null=True, blank=True)
    dt_demissao = models.DateField('Data Demissão', null=True, blank=True)
    ind_vinc = models.CharField('Indicador Vínculo', max_length=1, null=True, blank=True)
    tipo_ato_nom = models.CharField('Tipo Ato Nomeação', max_length=1, null=True, blank=True)
    nm_ato_nom = models.CharField('Número Ato Nomeação', max_length=50, null=True, blank=True)
    dt_ato_nom = models.DateField('Data Ato Nomeação', null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Funcionário MANAD'
        verbose_name_plural = 'Funcionários MANAD'
        indexes = [
            models.Index(fields=['cod_reg_trab', 'cpf']),
            models.Index(fields=['importacao', 'cod_reg_trab']),
        ]
    
    def __str__(self):
        return f"{self.cod_reg_trab} - {self.nome_trab}"


class ManadLotacao(models.Model):
    """Registro K100 - Lotação"""
    importacao = models.ForeignKey(ImportacaoManad, on_delete=models.CASCADE, related_name='lotacoes')
    tipo_registro = models.CharField('Tipo Registro', max_length=4, default='K100')
    dt_inc_alt = models.DateField('Data Inclusão/Alteração', null=True, blank=True)
    cod_ltc = models.CharField('Código Lotação', max_length=10, null=True, blank=True)
    cnpj_cei = models.CharField('CNPJ/CEI', max_length=14, null=True, blank=True)
    desc_ltc = models.CharField('Descrição Lotação', max_length=255, null=True, blank=True)
    cnpj_cei_tom = models.CharField('CNPJ/CEI Tomador', max_length=14, null=True, blank=True)
    lotacao = models.ForeignKey(Lotacao, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Lotação MANAD'
        verbose_name_plural = 'Lotações MANAD'
        unique_together = ['importacao', 'cod_ltc']
    
    def __str__(self):
        return f"{self.cod_ltc} - {self.desc_ltc}"


class ManadEventoFolha(models.Model):
    """Registro K150 - Rubricas (Eventos da folha de pagamento)"""
    importacao = models.ForeignKey(ImportacaoManad, on_delete=models.CASCADE, related_name='eventos_folha')
    tipo_registro = models.CharField('Tipo Registro', max_length=4, default='K150')
    cnpj_cei = models.CharField('CNPJ/CEI', max_length=14, null=True, blank=True)
    dt_inc_alt = models.DateField('Data Inclusão/Alteração', null=True, blank=True)
    cod_rubrica = models.CharField('Código Rubrica', max_length=10, null=True, blank=True)
    desc_rubrica = models.CharField('Descrição Rubrica', max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Evento Folha MANAD'
        verbose_name_plural = 'Eventos Folha MANAD'
        unique_together = ['importacao', 'cod_rubrica']
        indexes = [
            models.Index(fields=['cod_rubrica']),
        ]
    
    def __str__(self):
        return f"{self.cod_rubrica} - {self.desc_rubrica}"


class ManadDadosLaborais(models.Model):
    """Registro K250 - Mestre de folha de pagamento"""
    importacao = models.ForeignKey(ImportacaoManad, on_delete=models.CASCADE, related_name='dados_laborais')
    tipo_registro = models.CharField('Tipo Registro', max_length=4, default='K250')
    cnpj_cei = models.CharField('CNPJ/CEI', max_length=14, null=True, blank=True)
    ind_fl = models.CharField('Indicador Tipo Folha', max_length=1, null=True, blank=True)
    cod_ltc = models.CharField('Código Lotação', max_length=10, null=True, blank=True)
    cod_reg_trab = models.CharField('Código Registro Trabalhador', max_length=20, null=True, blank=True)
    dt_comp = models.CharField('Data Competência (MMAAAA)', max_length=6, null=True, blank=True)
    dt_pgto = models.DateField('Data Pagamento', null=True, blank=True)
    cod_cbo = models.CharField('Código CBO', max_length=6, null=True, blank=True)
    cod_ocorr = models.CharField('Código Ocorrência', max_length=2, null=True, blank=True)
    desc_cargo = models.CharField('Descrição Cargo', max_length=255, null=True, blank=True)
    qtd_dep_ir = models.IntegerField('Quantidade Dependentes IR', default=0)
    qtd_dep_sf = models.IntegerField('Quantidade Dependentes SF', default=0)
    vl_base_irrf = models.DecimalField('Valor Base IRRF', max_digits=12, decimal_places=2, default=0)
    vl_base_ps = models.DecimalField('Valor Base Previdência Social', max_digits=12, decimal_places=2, default=0)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True)
    lotacao = models.ForeignKey(Lotacao, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Dados Laborais MANAD'
        verbose_name_plural = 'Dados Laborais MANAD'
        indexes = [
            models.Index(fields=['importacao', 'cod_reg_trab', 'dt_comp']),
            models.Index(fields=['cod_reg_trab', 'dt_comp']),
        ]
    
    def __str__(self):
        return f"{self.cod_reg_trab} - {self.desc_cargo} - {self.dt_comp}"


class ManadLancamentoFolha(models.Model):
    """Registro K300 - Itens de folha de pagamento"""
    TIPO_LANCAMENTO = (
        ('P', 'Provento ou Vantagem'),
        ('D', 'Desconto'),
        ('O', 'Outros'),
    )
    
    importacao = models.ForeignKey(ImportacaoManad, on_delete=models.CASCADE, related_name='lancamentos_folha')
    tipo_registro = models.CharField('Tipo Registro', max_length=4, default='K300')
    cnpj_cei = models.CharField('CNPJ/CEI', max_length=14, null=True, blank=True)
    ind_fl = models.CharField('Indicador Tipo Folha', max_length=1, null=True, blank=True)
    cod_ltc = models.CharField('Código Lotação', max_length=10, null=True, blank=True)
    cod_reg_trab = models.CharField('Código Registro Trabalhador', max_length=20, null=True, blank=True)
    dt_comp = models.CharField('Data Competência (MMAAAA)', max_length=6, null=True, blank=True)
    cod_rubr = models.CharField('Código Rubrica', max_length=10, null=True, blank=True)
    vlr_rubr = models.DecimalField('Valor Rubrica', max_digits=12, decimal_places=2, default=0)
    ind_rubr = models.CharField('Indicador Rubrica', max_length=1, choices=TIPO_LANCAMENTO, null=True, blank=True)
    ind_base_irrf = models.CharField('Indicador Base IRRF', max_length=1, null=True, blank=True)
    ind_base_ps = models.CharField('Indicador Base PS', max_length=1, null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    evento_folha = models.ForeignKey(ManadEventoFolha, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Lançamento Folha MANAD'
        verbose_name_plural = 'Lançamentos Folha MANAD'
        indexes = [
            models.Index(fields=['importacao', 'cod_reg_trab', 'dt_comp']),
            models.Index(fields=['cod_reg_trab', 'cod_rubr']),
            models.Index(fields=['ind_rubr']),
        ]
    
    def __str__(self):
        return f"{self.cod_reg_trab} - {self.cod_rubr} - {self.vlr_rubr}"
