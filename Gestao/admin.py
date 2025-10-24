from django.contrib import admin
from .models import Dre, Conta, Orcamento, Lancamento, Dfc, Banco, Conta_Financeira, CentroCusto, ConfigGeral, Fornecedor, reponsavel_conta
from django.contrib.admin.filters import SimpleListFilter
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .admin_mixins import DateHierarchyCurrentMonthMixin
from django import forms
# Register your models here.


def limparConfDre(modeladmin, request, queryset):
    for conta in queryset:
        Conta.objects.filter(codigo=conta.codigo).update(dre=None)
    modeladmin.message_user(request, "Configuração da DRE removida com sucesso!!!")
    
limparConfDre.short_description='Limpar código DRE'    


def geraOrcMesSeguinte(modeladmin, request, queryset):
    
    ultimaData = Orcamento.objects.raw("""
                                        select e.id, max(data) data 
                                        from SISEVOL..RH_empresa e 
                                        join sisevol..gestao_orcamento o on o.empresa_id = e.id
                                        group by e.id
                                        """)
                                            
    
    
    for orc in queryset:
        dt = None
        for rec in ultimaData:
            if rec.id == orc.empresa.id:
                dt = rec.data
                print(rec.data)

        novo_registro = Orcamento(
            data = dt + relativedelta(months=1),
            valor = orc.valor,
            conta = orc.conta,
            centro_custo = orc.centro_custo,
            empresa = orc.empresa
        )
        
        print(novo_registro)
        novo_registro.save()
        
    modeladmin.message_user(request, "Orçamento gerado com sucesso!!!")
    
geraOrcMesSeguinte.short_description='Gerar Orçamento Mês Seguinte'    


class filterDre(admin.SimpleListFilter):
    title = 'DRE'
    parameter_name = 'dre'
    
    def lookups(self, request, model_admin):
        lista = Conta.objects.raw("select distinct d.id, d.nivel from gestao_conta c join gestao_dre d on d.id = c.dre_id ") 
        return [(x.id, x.nivel) for x in lista]
    
    def queryset(self, request, queryset):
        if self.value():   
            return queryset.filter(dre=self.value())
        
        return queryset
      
class filterDfc(admin.SimpleListFilter):
    title = 'DFC'
    parameter_name = 'dfc'
    
    def lookups(self, request, model_admin):
        lista = Conta.objects.raw("select distinct d.id, d.dfc from gestao_conta c join gestao_dfc d on d.id = c.dfc_id ") 
        return [(x.id, x.dfc) for x in lista]
    
    def queryset(self, request, queryset):
        if self.value():   
            return queryset.filter(dfc=self.value())
        
        return queryset        
   
    
class filterMesOrc(admin.SimpleListFilter):
    title = 'Meses'
    parameter_name = 'mes'
    
    def lookups(self, request, model_admin):
        lista = Conta.objects.raw("select distinct mesNumero id, mes nome from SISEVOL..Gestao_orcamento o join dw_bi..DimData d on d.data = o.data order by 1") 
        return [(x.id, x.nome ) for x in lista]
    
    def queryset(self, request, queryset):
        if self.value():   
            return queryset.filter(data__month=self.value())
        
        return queryset    
    
class filterAnoOrc(admin.SimpleListFilter):
    title = 'Ano'
    parameter_name = 'ano'
    
    def lookups(self, request, model_admin):
        lista = Conta.objects.raw("select distinct ano id, ano nome from SISEVOL..Gestao_orcamento o join dw_bi..DimData d on d.data = o.data order by 1") 
        return [(x.id, x.nome ) for x in lista]
    
    def queryset(self, request, queryset):
        if self.value():   
            return queryset.filter(data__year=self.value())
        
        return queryset        
 
class filterNivel1Orc(admin.SimpleListFilter):
    title = 'Nivel 1'
    parameter_name = 'nivel1'
    
    def lookups(self, request, model_admin):
        lista = Conta.objects.raw("select codigo id, codigo+' - '+nome nome from SISEVOL..Gestao_conta where nivel = 1") 
        return [(x.id, x.nome ) for x in lista]
    
    def queryset(self, request, queryset):
        if self.value():   
            return  queryset.filter(conta__codigo__startswith=self.value())
        
        return queryset             

class filterNivel1Conta(admin.SimpleListFilter):
    title = 'Nivel 1'
    parameter_name = 'nivel1'
    
    def lookups(self, request, model_admin):
        lista = Conta.objects.raw("select codigo id, codigo+' - '+nome nome from SISEVOL..Gestao_conta where nivel = 1") 
        return [(x.id, x.nome ) for x in lista]
    
    def queryset(self, request, queryset):
        if self.value():   
            return  queryset.filter(codigo__startswith=self.value())
        
        return queryset          

@admin.register(Dre)
class DreAdmin(admin.ModelAdmin):
    fields = ['codigo','nome']
    list_display = ['codigo','nome', 'nivel']
    
    
@admin.register(Dfc)
class DfcAdmin(admin.ModelAdmin):
    fields = ['codigo','nome', 'nivel1', 'nivel2']
    list_display = ['id','codigo','nome', 'nivel1', 'nivel2']


@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    
    def dre_nome(self, obj):
        print(self.dre_nivel)
        return obj  # Exibe o nome do Dre relacionado
    dre_nome.admin_order_field = 'dre'  # Permite ordenar pela chave estrangeira
    
    # fields = ['codigo', 'nome', 'solucao',  'dre_nome', 'analitica', 'natureza']
    list_display = ['codigo','nome', 'nivel','solucao', 'mae', 'dre','dfc', 'nivel_dre', 'analitica', 'natureza', 'operacao']
    actions = [limparConfDre]
    list_filter = ('nivel','analitica','natureza',filterDre,  filterNivel1Conta)
    ordering = ('ordem',)
    search_fields = ('nome','codigo') 
        
    fieldsets = (
        (None, {'fields': ('codigo', 'nome', 'solucao',  'dre', 'dfc', 'nivel_dre', 'analitica', 'natureza', 'operacao', 'cenario')}),
    )
    
    
def recalcularOtimistaRealista(modeladmin, request, queryset):
    """Recalcula automaticamente os campos otimista e realista apenas se estiverem vazios ou zerados e apenas para contas com cenário=True"""
    contador = 0
    
    conf_pessimista = float(ConfigGeral.objects.get(parametro='PERCENTUAL_PESSIMISTA').valor) / 100
    conf_otimista = float(ConfigGeral.objects.get(parametro='PERCENTUAL_OTIMISTA').valor) / 100

    print(50*'*')
    for orcamento in queryset:
        print(orcamento.conta.cenario)
        print(orcamento.valor)
        print(orcamento.pessimista)
        print(orcamento.otimista)
        print(50*'*')
        # Verifica se a conta tem cenário=True
        if orcamento.conta.cenario and orcamento.valor > 0:
            modificado = False
            
            print(50*'*')
            # Se pessimista está vazio ou zero, calcular como 80% do valor
            orcamento.pessimista = orcamento.valor - (abs(orcamento.valor) * conf_pessimista)
            modificado = True
            print(orcamento.pessimista)
            
            
            orcamento.otimista = orcamento.valor + (abs(orcamento.valor) * conf_otimista)
            modificado = True
            print(orcamento.otimista)
            
            if modificado:
                orcamento.save()
                contador += 1
    
    if contador > 0:
        modeladmin.message_user(request, f"Recalculados {contador} registros com sucesso!")
    else:
        modeladmin.message_user(request, "Nenhum registro precisou ser recalculado.")
    
recalcularOtimistaRealista.short_description = 'Recalcular Otimista e Realista (apenas vazios)'
    
    
@admin.register(Orcamento)
class OrcamentoAdmin(DateHierarchyCurrentMonthMixin, admin.ModelAdmin):
    
    list_display = ['empresa','data','conta','centro_custo','valor','observacao']
    list_filter = ['empresa', filterAnoOrc,filterMesOrc, filterNivel1Orc]
    actions = [geraOrcMesSeguinte, recalcularOtimistaRealista]
    search_fields = ('conta__nome',) 
    list_editable = ('valor','centro_custo')
    list_per_page = 500
    date_hierarchy = 'data'
    
    def save_model(self, request, obj, form, change):
        """Sobrescreve o save para calcular automaticamente otimista e realista se estiverem vazios e apenas para contas com cenário=True"""
        
        conf_pessimista = float(ConfigGeral.objects.get(parametro='PERCENTUAL_PESSIMISTA').valor) / 100
        conf_otimista = float(ConfigGeral.objects.get(parametro='PERCENTUAL_OTIMISTA').valor) / 100
        # Calcular otimista e realista apenas se estiverem em branco ou zerados e apenas para contas com cenário=True
        if obj.conta.cenario and obj.valor and obj.valor > 0:
            # Se pessimista está vazio ou zero, calcular como 80% do valor
            if not obj.pessimista or obj.pessimista == 0:
                obj.pessimista = obj.valor - (abs(obj.valor) * conf_pessimista)
            
            # Se otimista está vazio ou zero, calcular como 120% do valor
            if not obj.otimista or obj.otimista == 0:
                obj.otimista = obj.valor + (abs(obj.valor) * conf_otimista)
        
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        """Sobrescreve o save_formset para calcular automaticamente em mudanças em lote e apenas para contas com cenário=True"""
        instances = formset.save(commit=False)
        
        for instance in instances:
            if instance.conta.cenario and instance.valor and instance.valor > 0:
                # Se pessimista está vazio ou zero, calcular como 80% do valor
                if not instance.pessimista or instance.pessimista == 0:
                    instance.pessimista = instance.valor * 0.80
                
                # Se otimista está vazio ou zero, calcular como 120% do valor
                if not instance.otimista or instance.otimista == 0:
                    instance.otimista = instance.valor * 1.20
        
        formset.save()
        super().save_formset(request, form, formset, change)
  
    
    def changelist_view(self, request, extra_context=None):
        """
        Sobrescreve a view para incluir o token CSRF
        """
        extra_context = extra_context or {}
        extra_context['csrf_token'] = request.META.get('CSRF_COOKIE', '')
        return super().changelist_view(request, extra_context)
    
    class Media:
        css = {
            'all': ('css/admin_orcamento.css',)
        }
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'js/formatacao.js',
            'js/adminOrc.js',)    




class filterMesLan(admin.SimpleListFilter):
    title = 'Meses'
    parameter_name = 'mes'
    
    def lookups(self, request, model_admin):
        lista = Conta.objects.raw("select distinct mesNumero id, mes nome from SISEVOL..Gestao_lancamento o join dw_bi..DimData d on d.data = o.data order by 1") 
        return [(x.id, x.nome ) for x in lista]
    
    def queryset(self, request, queryset):
        if self.value():   
            return queryset.filter(data__month=self.value())
        
        return queryset    
    
class filterAnoLan(admin.SimpleListFilter):
    title = 'Ano'
    parameter_name = 'ano'
    
    def lookups(self, request, model_admin):
        lista = Conta.objects.raw("select distinct ano id, ano nome from SISEVOL..Gestao_lancamento o join dw_bi..DimData d on d.data = o.data order by 1") 
        return [(x.id, x.nome ) for x in lista]
    
    def queryset(self, request, queryset):
        if self.value():   
            return queryset.filter(data__year=self.value())
        
        return queryset        

def geraLancMesSeguinte(modeladmin, request, queryset):
    
    ultimaData = Lancamento.objects.raw("""
                                        select e.id, conta_id, max(data) data 
                                        from SISEVOL..RH_empresa e 
                                        join sisevol..gestao_lancamento o on o.empresa_id = e.id
                                        group by e.id, conta_id
                                        """)
    for orc in queryset:
        dt = None
        for rec in ultimaData:
            if rec.id == orc.empresa.id and rec.conta_id == orc.conta.id:
                dt = rec.data
                print(rec.data)

        novo_registro = Lancamento(
            data = dt + relativedelta(months=1),
            valor = orc.valor,
            conta = orc.conta,
            empresa = orc.empresa
        )
        
        print(novo_registro)
        novo_registro.save()
        
    modeladmin.message_user(request, "Lancamento Mês Seguinte gerado com sucesso!!!")
    
geraLancMesSeguinte.short_description='Gerar Lançamento Mês Seguinte'    


@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = ['empresa','data','conta','valor']
    list_filter = ['empresa', filterAnoLan, filterMesLan ]
    search_fields = ('conta__nome','conta__codigo')
    actions = [geraLancMesSeguinte]
    

    
        
@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ['id','banco']        

@admin.register(Conta_Financeira)
class Conta_FinanceiraAdmin(admin.ModelAdmin):
    list_display = ['conta','empresa','data','saldo_formatado']   
    
    def saldo_formatado(self, obj) :
        return '{:,.2f}'.format(obj.saldo_inicial).replace(',', 'v').replace('.', ',').replace('v', '.')
    
    
    
    
@admin.register(CentroCusto)
class CentroCustoAdmin(admin.ModelAdmin):
    list_display = ['codigo','nome', 'parent']
    
@admin.register(ConfigGeral)
class ConfigGeralAdmin(admin.ModelAdmin):
    list_display = ['parametro','valor', 'usuario', 'created', 'updated']
    list_filter = ['usuario', 'created', 'updated']
    search_fields = ['parametro', 'valor', 'usuario__username']
    readonly_fields = ['created', 'updated']
    ordering = ['-created']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('parametro', 'valor')
        }),
       
    )
    
    def save_model(self, request, obj, form, change):
        """Sobrescreve o save para preencher automaticamente o usuário"""
        if not change:  # Se é um novo registro
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Filtra os registros para mostrar apenas os do usuário atual"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusuários veem todos os registros
        return qs.filter(usuario=request.user)
    
    def get_form(self, request, obj=None, **kwargs):
        """Personaliza o formulário para esconder o campo usuario em novos registros"""
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Se é um novo registro
            if 'usuario' in form.base_fields:
                form.base_fields['usuario'].widget = forms.HiddenInput()
        else:  # Se é uma edição
            if 'usuario' in form.base_fields:
                form.base_fields['usuario'].widget.attrs['readonly'] = True
                form.base_fields['usuario'].help_text = 'Usuário que criou este registro (não pode ser alterado)'
        return form
    
    def has_change_permission(self, request, obj=None):
        """Permite edição apenas para o usuário que criou ou superusuários"""
        if obj is None:
            return True
        return request.user.is_superuser or obj.usuario == request.user
    
    def has_delete_permission(self, request, obj=None):
        """Permite exclusão apenas para o usuário que criou ou superusuários"""
        if obj is None:
            return True
        return request.user.is_superuser or obj.usuario == request.user



@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['codigo','nome']
    
    
@admin.register(reponsavel_conta)
class reponsavel_contaAdmin(admin.ModelAdmin):
    list_display = ['empresa','conta','responsavel']
    list_filter = ['empresa','conta','responsavel']
    search_fields = ['empresa__empresa','conta__nome','responsavel__username']
    list_per_page = 500
    ordering = ['empresa','conta','responsavel']
    readonly_fields = ['created', 'updated']
    list_editable = ['responsavel']
    list_display_links = ['empresa','conta']
    list_select_related = ['empresa','conta','responsavel']
    list_filter = ['empresa','conta','responsavel']