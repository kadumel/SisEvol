from django.contrib import admin
from django.utils import timezone
from datetime import datetime

class DateHierarchyCurrentMonthMixin:
    """
    Mixin para configurar automaticamente a date_hierarchy para o mês atual
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
            from urllib.parse import urlencode
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
            from django.http import HttpResponseRedirect
            from django.urls import reverse
            url = reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist')
            if params:
                url += '?' + urlencode(params)
            
            return HttpResponseRedirect(url)
        
        return super().changelist_view(request, extra_context) 