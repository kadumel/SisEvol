from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Obtém um item de um dicionário por chave"""
    return dictionary.get(key, 0)

@register.filter
def values(dictionary):
    """Retorna todos os valores de um dicionário"""
    return dictionary.values()

@register.filter
def month_name(month_number):
    """Converte número do mês em nome"""
    meses = {
        '1': 'Janeiro', '2': 'Fevereiro', '3': 'Março', '4': 'Abril',
        '5': 'Maio', '6': 'Junho', '7': 'Julho', '8': 'Agosto',
        '9': 'Setembro', '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
    }
    return meses.get(str(month_number), '')

@register.filter
def split(value, arg):
    """Divide uma string por um separador"""
    return value.split(arg)

@register.filter
def format_currency(value):
    """Formata valor como moeda brasileira com pontos de milhar (sem R$)"""
    if value is None or value == 0:
        return "0,00"
    
    try:
        valor_float = float(value)
        valor_formatado = "{:,.2f}".format(valor_float)
        valor_formatado = valor_formatado.replace(",", "X").replace(".", ",").replace("X", ".")
        return valor_formatado
    except (ValueError, TypeError):
        return "0,00"

@register.filter
def mul(value, arg):
    """Multiplica dois valores"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0 

@register.filter
def format_percent(value):
    """Formata valor como percentual"""
    if value is None:
        return "0,00%"
    
    try:
        valor_float = float(value)
        return f"{valor_float:.2f}%".replace(".", ",")
    except (ValueError, TypeError):
        return "0,00%" 