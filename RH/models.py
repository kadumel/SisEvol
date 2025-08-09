from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.

SEXO_CHOICES = (
    ("M", "Masculino"),
    ("F", "Feminino"),
    ("T", "Todes")
)

TIPO_STATUS = (
    ("A","ATIVO"),
    ("F","AFASTADO"),
    ("D", "DEMITIDO")
)

BANCO_CHOICES = (
    ("BANCO DO BRASIL", "BANCO DO BRASIL"),
    ("CAIXA ECONOMICA", "CAIXA ECONOMICA"),
    ("ITAU", "ITAU"),
    ("BRADESCO", "BRADESCO"),
    ("SANTANDER", "SANTANDER"),
    ("NUBANK", "NUBANK"),
    ("INTER", "INTER")
)

YES_NO_CHOICE = (
    ("S", "SIM"),
    ("N", "NÃO")
)

SEMANA_CHOICE = (
    ("SEGUNDA-FEIRA", "SEGUNDA-FEIRA"),
    ("TERÇA-FEIRA", "TERÇA-FEIRA"),
    ("QUARTA-FEIRA", "QUARTA-FEIRA"),
    ("QUINTA-FEIRA", "QUINTA-FEIRA"),
    ("SEXTA-FEIRA", "SEXTA-FEIRA"),
    ("SABADO", "SABADO"),
    ("DOMINGO", "DOMINGO"),
)

FREQUENCIA_CHOICES = (
    ("P", "PRESENTE"),
    ("F", "FALTA"),
    ("J", "JUSTIFICADA"),
    ("A", "ATRASO"),
    ("S", "SAÍDA_ANTECIPADA"),
)



class Empresa(models.Model):
    codigo_BI = models.IntegerField()
    empresa = models.CharField(max_length=100, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.empresa}"
    

class Lotacao(models.Model):
    lotacao = models.CharField(max_length=100, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.lotacao}"

class Cargo(models.Model):
    cargo = models.CharField(max_length=100, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.cargo}"
    
    
class Folga(models.Model):
    folga = models.CharField(max_length=100, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.folga}"    
    
    

class TipoContrato(models.Model):
    tipo_contrato = models.CharField(max_length=100, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.tipo_contrato}"
    
class Banco(models.Model):
    banco = models.CharField(max_length=30, choices=BANCO_CHOICES)
    agencia = models.CharField(max_length=20,  blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.banco} - {self.agencia}"
    
class Turno(models.Model):
    turno = models.CharField(max_length=100,  blank=False, null=False)
    intervalo = models.CharField(max_length=20,  blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.turno} - {self.intervalo}"

    
    
class Funcionario(models.Model):
    empresa = models.ForeignKey('Empresa', Empresa)
    matricula = models.CharField('Matrícula',max_length=6, null=True, blank=True)
    dt_admissao = models.DateField('Data Admissão',  null=True, blank=True)
    dt_demissao = models.DateField('Data Demissão', null=True, blank=True)
    nome = models.CharField('Nome',max_length=100)
    dt_nascimento = models.DateField('Data Nascimento', null=True, blank=True)
    sexo = models.CharField('Sexo',max_length=1,choices=SEXO_CHOICES)
    naturalidade = models.CharField('Naturalidade',max_length=40, null=True, blank=True)
    rg = models.CharField('RG',max_length=20, null=True, blank=True)
    cpf = models.CharField('CPF', max_length=14, null=True, blank=True)
    conta_bancaria = models.CharField('Conta Bancária',max_length=20, null=True, blank=True)
    cargo = models.ForeignKey('Cargo', Cargo, null=True, blank=True)
    lotacao = models.ForeignKey('Lotacao', Lotacao, null=True, blank=True)
    #gestor = models.ForeignKey('Gestor', gestor)
    tipo_contrato = models.ForeignKey('TipoContrato',TipoContrato, null=True, blank=True)
    turno = models.ForeignKey('Turno',Turno, null=True, blank=True)
    motivo_contratacao = models.CharField('Motivo da Contração',max_length=80, null=True, blank=True)
    dt_primeiro_termino = models.DateField('Data 1º Termino', null=True, blank=True)
    dt_segundo_termino = models.DateField('Data 2º Termino', null=True, blank=True)
    dt_contrato_experiencia = models.DateField('Data Contrato Experiência', null=True, blank=True)
    dt_ultimo_aso = models.DateField('Data Último ASO', null=True, blank=True)
    dt_aso_periodico = models.DateField('Data ASO Periódico', null=True, blank=True)
    fone_fixo = models.CharField('Fone Fixo',max_length=20, null=True, blank=True)
    fone_celular = models.CharField('Fone Celular',max_length=20, null=True, blank=True)
    folga = models.ForeignKey('Folga', Folga, null=True, blank=True)
    plano_saude_titular = models.CharField('Plano de Saúde Titular',max_length=1,choices=YES_NO_CHOICE, null=True, blank=True)
    plano_saude_dependente = models.CharField('Plano de Saúde Dependente',max_length=1,choices=YES_NO_CHOICE, null=True, blank=True)
    plano_odonto_titular = models.CharField('Plano Odonto Titular',max_length=1,choices=YES_NO_CHOICE, null=True, blank=True)
    plano_odonto_dependente = models.CharField('Plano Odonto Dependente',max_length=1,choices=YES_NO_CHOICE, null=True, blank=True)
    vale_transporte = models.CharField('Vale Transporte',max_length=1,choices=YES_NO_CHOICE, null=True, blank=True)
    salario_familia = models.CharField('Salário Família',max_length=1,choices=YES_NO_CHOICE, null=True, blank=True)
    dependentes = models.CharField('Dependente',max_length=1,choices=YES_NO_CHOICE, null=True, blank=True)
    salario_fixo = models.FloatField('Salário Fixo',default=0)
    salario_compl = models.FloatField('Salário Complementar', default=0)
    deleted = models.CharField(max_length=1, default='N',  null=True, blank=True)
    status = models.CharField(max_length=1, default='A', choices=TIPO_STATUS)
    dt_integracao = models.DateField('Data Integração', null=True, blank=True)
    ajuda_custo = models.FloatField('Ajuda de Custo',default=0)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.matricula} - {self.nome}"
    

class Vaga(models.Model):
    pass

class ConfigGeral(models.Model):
    empresa = models.ForeignKey('Empresa', Empresa)
    dias_primeiro_termino_exp = models.IntegerField()
    dias_segundo_termino_exp = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.empresa.empresa} - {self.dias_primeiro_termino_exp} - {self.dias_segundo_termino_exp}"
    

class Gestor(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    funcionario = models.ForeignKey('Funcionario',Funcionario)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.cargo.cargo} - {self.funcionario.nome}"


class TipoEvento(models.Model):
    tipo_evento = models.CharField('Tipo Evento', max_length=40)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.tipo_evento}"
    
class Evento(models.Model):
    tipo = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
    descricao = models.CharField('Descrição', max_length=50)
    Obs = models.TextField('Observação',max_length=250)
    vagas = models.IntegerField('Vagas', null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.tipo.tipo_evento} - {self.descricao}"


class DiaEvento(models.Model):
    """Modelo para controlar os dias específicos de um evento"""
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='dias_evento')
    data = models.DateField('Data do Dia', null=False, blank=False)
    hora_inicio = models.TimeField('Hora de Início', null=True, blank=True)
    hora_fim = models.TimeField('Hora de Fim', null=True, blank=True)
    observacoes = models.TextField('Observações', max_length=500, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        unique_together = ['evento', 'data']
        ordering = ['data', 'hora_inicio']
    
    def __str__(self):
        return f"{self.evento.descricao} - {self.data} "
    

class ControleEvento(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.funcionario.nome} - {self.evento.descricao}"


class FrequenciaEvento(models.Model):
    """Modelo para controlar a frequência dos funcionários nos dias dos eventos"""
    controle_evento = models.ForeignKey(ControleEvento, on_delete=models.CASCADE, related_name='frequencias')
    dia_evento = models.ForeignKey(DiaEvento, on_delete=models.CASCADE, related_name='frequencias')
    status = models.CharField('Status', max_length=1, choices=FREQUENCIA_CHOICES, default='P')
    hora_entrada = models.TimeField('Hora de Entrada', null=True, blank=True)
    hora_saida = models.TimeField('Hora de Saída', null=True, blank=True)
    observacoes = models.TextField('Observações', max_length=500, null=True, blank=True)
    usuario_registro = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='frequencias_registradas')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        unique_together = ['controle_evento', 'dia_evento']
        ordering = ['dia_evento__data', 'controle_evento__funcionario__nome']
    
    def __str__(self):
        return f"{self.controle_evento.funcionario.nome} - {self.dia_evento}"
    


    
    
class Auditoria(models.Model):
    origem = models.CharField(max_length=50)  # Controle de Visitante
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False) # Daniel
    observacao = models.TextField(max_length=4000, null=True, blank=True) 
    createDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.origem} - {self.usuario} - {self.observacao}"

    

class Absenteismo(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data = models.DateField('Data', null=False, blank=False)
    dias_trabalho = models.IntegerField('Dias Trabalho', null=False, blank=False)
    dias_falta = models.IntegerField('Dias Falta', null=False, blank=False)
    dias_justificados = models.IntegerField('Dias Justificados', null=False, blank=False)
    dias_atraso = models.IntegerField('Dias Atraso', null=False, blank=False)
    dias_saida_antecipada = models.IntegerField('Dias Saída Antecipada', null=False, blank=False)
    dias_extras = models.IntegerField('Dias Extras', null=False, blank=False)
    dias_ferias = models.IntegerField('Dias Férias', null=False, blank=False)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        unique_together = ['funcionario', 'data']
        ordering = ['data','funcionario']
        db_table = 'absenteismo'
        
    def __str__(self):
        return f"{self.funcionario.nome} - {self.data}"
    
    
    