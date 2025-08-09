from django.contrib import admin
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class DateHierarchyCurrentMonthMixin:
    """
    Mixin global para configurar automaticamente a date_hierarchy para o mês atual
    """
    
    def changelist_view(self, request, extra_context=None):
        """
        Sobrescreve a view para configurar automaticamente o mês atual na date_hierarchy
        """
        # Verificar se há parâmetros de data na URL
        data_params = [
            'data__year', 'data__month', 'data__day',
            'dia_evento__data__year', 'dia_evento__data__month', 'dia_evento__data__day'
        ]
        
        has_date_params = any(param in request.GET for param in data_params)
        
        # Se não há parâmetros de data, redirecionar para o mês atual
        if not has_date_params and hasattr(self, 'date_hierarchy'):
            hoje = timezone.now()
            ano_atual = hoje.year
            mes_atual = hoje.month
            
            # Construir a nova URL com os parâmetros de data
            params = request.GET.copy()
            
            # Determinar qual campo de data usar baseado na date_hierarchy
            if self.date_hierarchy == 'data':
                params['data__year'] = ano_atual
                params['data__month'] = mes_atual
            elif self.date_hierarchy == 'dia_evento__data':
                params['dia_evento__data__year'] = ano_atual
                params['dia_evento__data__month'] = mes_atual
            
            # Remover parâmetros vazios
            params = {k: v for k, v in params.items() if v}
            
            # Construir nova URL
            url = reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist')
            if params:
                url += '?' + urlencode(params)
            
            return HttpResponseRedirect(url)
        
        return super().changelist_view(request, extra_context)

# Configuração personalizada do UserAdmin para resolver problemas de permissões
class CustomUserAdmin(UserAdmin):
    """
    Configuração personalizada do UserAdmin para resolver problemas de acesso às permissões
    """
    
    def get_fieldsets(self, request, obj=None):
        """
        Sobrescreve os fieldsets para garantir que as permissões sejam exibidas corretamente
        """
        if not obj:  # Se é um novo usuário
            return self.add_fieldsets
        else:  # Se é uma edição
            return (
                (None, {'fields': ('username', 'password')}),
                ('Informações pessoais', {'fields': ('first_name', 'last_name', 'email')}),
                ('Permissões2', {
                    'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                    'classes': ('collapse',),
                }),
                ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
            )
    
    def get_readonly_fields(self, request, obj=None):
        """
        Define campos somente leitura
        """
        if obj:  # Se é uma edição
            return ('last_login', 'date_joined')
        return ()
    
    def has_module_permission(self, request):
        """
        Verifica se o usuário tem permissão para acessar o módulo
        """
        return request.user.is_staff
    
    def has_view_permission(self, request, obj=None):
        """
        Verifica se o usuário tem permissão para visualizar
        """
        return request.user.is_staff
    
    def has_add_permission(self, request):
        """
        Verifica se o usuário tem permissão para adicionar
        """
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        """
        Verifica se o usuário tem permissão para alterar
        """
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        """
        Verifica se o usuário tem permissão para deletar
        """
        return request.user.is_staff

# Função para aplicar o mixin automaticamente a todas as classes admin que usam date_hierarchy
def apply_date_hierarchy_mixin():
    """
    Aplica automaticamente o DateHierarchyCurrentMonthMixin a todas as classes admin
    que possuem date_hierarchy configurado
    """
    for model_admin in admin.site._registry.values():
        if hasattr(model_admin, 'date_hierarchy') and model_admin.date_hierarchy:
            # Verificar se já não tem o mixin aplicado
            if not any(issubclass(base, DateHierarchyCurrentMonthMixin) for base in model_admin.__class__.__bases__):
                # Criar uma nova classe que herda do mixin e da classe original
                bases = (DateHierarchyCurrentMonthMixin,) + model_admin.__class__.__bases__
                new_class = type(
                    model_admin.__class__.__name__,
                    bases,
                    dict(model_admin.__class__.__dict__)
                )
                
                # Substituir a classe no registro
                admin.site._registry[model_admin.model] = new_class(model_admin.model, admin.site)

# Registrar o CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin) 