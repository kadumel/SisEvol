from django.contrib import admin
from .models import ImportacaoManad, ManadCabecalho, ManadEmpresa, ManadFuncionario, ManadDadosLaborais, ManadLancamentoFolha, ManadEventoFolha, ManadLotacao
# Register your models here.
@admin.register(ImportacaoManad)
class ImportacaoManadAdmin(admin.ModelAdmin):
    list_display = ('arquivo', 'data_importacao', 'status')
    list_filter = ('status',)
    search_fields = ('arquivo',)
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('status',)
    list_display_links = ('arquivo',)
    list_select_related = True
    
    
@admin.register(ManadCabecalho)
class ManadCabecalhoAdmin(admin.ModelAdmin):
    list_display = ('importacao', 'tipo_registro', 'nome', 'cnpj', 'cpf', 'cei', 'nit', 'uf', 'ie', 'cod_mun', 'im', 'suframa', 'ind_centr', 'dt_ini', 'dt_fin', 'cod_ver', 'cod_fin', 'ind_ed')
    list_filter = ('importacao', 'tipo_registro')
    search_fields = ('nome', 'cnpj', 'cpf', 'cei', 'nit', 'uf', 'ie', 'cod_mun', 'im', 'suframa', 'ind_centr', 'dt_ini', 'dt_fin', 'cod_ver', 'cod_fin', 'ind_ed')
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('nome', 'cnpj', 'cpf', 'cei', 'nit', 'uf', 'ie', 'cod_mun', 'im', 'suframa', 'ind_centr', 'dt_ini', 'dt_fin', 'cod_ver', 'cod_fin', 'ind_ed')
    list_display_links = ('importacao', 'tipo_registro')
    list_select_related = True
    
    
@admin.register(ManadEmpresa)
class ManadEmpresaAdmin(admin.ModelAdmin):
    list_display = ('importacao', 'tipo_registro', 'emp_tec', 'cargo', 'dt_ini_serv_inf', 'dt_fim_serv_inf', 'cnpj', 'cpf', 'fone', 'fax', 'email')
    list_filter = ('importacao', 'tipo_registro')
    search_fields = ('emp_tec', 'cargo', 'cnpj', 'cpf', 'fone', 'fax', 'email')
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('emp_tec', 'cargo', 'dt_ini_serv_inf', 'dt_fim_serv_inf', 'cnpj', 'cpf', 'fone', 'fax', 'email')
    list_display_links = ('importacao', 'tipo_registro')
    list_select_related = True
    
@admin.register(ManadFuncionario)
class ManadFuncionarioAdmin(admin.ModelAdmin):
    list_display = ('importacao', 'tipo_registro', 'cnpj_cei', 'dt_inc_alt', 'cod_reg_trab', 'cpf', 'nit', 'cod_categ', 'nome_trab', 'dt_nasc', 'dt_admissao', 'dt_demissao', 'ind_vinc', 'tipo_ato_nom', 'nm_ato_nom', 'dt_ato_nom')
    list_filter = ('importacao', 'tipo_registro')
    search_fields = ('nome_trab', 'cpf', 'nit', 'cod_categ', 'nome_trab')
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('cnpj_cei', 'dt_inc_alt', 'cod_reg_trab', 'cpf', 'nit', 'cod_categ', 'nome_trab', 'dt_nasc', 'dt_admissao', 'dt_demissao', 'ind_vinc', 'tipo_ato_nom', 'nm_ato_nom', 'dt_ato_nom')
    list_display_links = ('importacao', 'tipo_registro')
    list_select_related = True
    
@admin.register(ManadDadosLaborais)
class ManadDadosLaboraisAdmin(admin.ModelAdmin):
    list_display = ('importacao', 'tipo_registro', 'cnpj_cei', 'ind_fl', 'cod_ltc', 'cod_reg_trab', 'dt_comp', 'dt_pgto', 'cod_cbo', 'cod_ocorr', 'desc_cargo', 'qtd_dep_ir', 'qtd_dep_sf', 'vl_base_irrf', 'vl_base_ps')
    list_filter = ('importacao', 'tipo_registro')
    search_fields = ('desc_cargo', 'cod_cbo', 'cod_ocorr', 'desc_cargo')
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('cnpj_cei', 'ind_fl', 'cod_ltc', 'cod_reg_trab', 'dt_comp', 'dt_pgto', 'cod_cbo', 'cod_ocorr', 'desc_cargo', 'qtd_dep_ir', 'qtd_dep_sf', 'vl_base_irrf', 'vl_base_ps')
    list_display_links = ('importacao', 'tipo_registro')
    list_select_related = True
    
@admin.register(ManadLancamentoFolha)   
class ManadLancamentoFolhaAdmin(admin.ModelAdmin):
    list_display = ('importacao', 'tipo_registro', 'cnpj_cei', 'ind_fl', 'cod_ltc', 'cod_reg_trab', 'dt_comp', 'cod_rubr', 'vlr_rubr', 'ind_rubr', 'ind_base_irrf', 'ind_base_ps')
    list_filter = ('importacao', 'tipo_registro')
    search_fields = ('cod_rubr', 'vlr_rubr', 'ind_rubr', 'ind_base_irrf', 'ind_base_ps')
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('cnpj_cei', 'ind_fl', 'cod_ltc', 'cod_reg_trab', 'dt_comp', 'cod_rubr', 'vlr_rubr', 'ind_rubr', 'ind_base_irrf', 'ind_base_ps')
    list_display_links = ('importacao', 'tipo_registro')
    list_select_related = True
    
@admin.register(ManadEventoFolha)   
class ManadEventoFolhaAdmin(admin.ModelAdmin):
    list_display = ('importacao', 'tipo_registro', 'cnpj_cei', 'dt_inc_alt', 'cod_rubrica', 'desc_rubrica')
    list_filter = ('importacao', 'tipo_registro')
    search_fields = ('desc_rubrica', 'cod_rubrica', 'desc_rubrica')
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('cnpj_cei', 'dt_inc_alt', 'cod_rubrica', 'desc_rubrica')
    list_display_links = ('importacao', 'tipo_registro')
    list_select_related = True
    
@admin.register(ManadLotacao)   
class ManadLotacaoAdmin(admin.ModelAdmin):
    list_display = ('importacao', 'tipo_registro', 'dt_inc_alt', 'cod_ltc', 'cnpj_cei', 'desc_ltc', 'cnpj_cei_tom', 'lotacao')
    list_filter = ('importacao', 'tipo_registro')
    search_fields = ('cod_ltc', 'desc_ltc', 'cnpj_cei', 'cnpj_cei_tom')
    list_per_page = 10
    list_max_show_all = 100
    # Apenas campos que existem em ManadLotacao e não estão em list_display_links
    list_editable = ('cod_ltc', 'cnpj_cei', 'desc_ltc', 'cnpj_cei_tom', 'lotacao')
    list_display_links = ('importacao', 'tipo_registro')
    list_select_related = True
    
    

    

    
    