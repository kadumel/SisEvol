from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retorna o valor de uma chave do dicionário"""
    return dictionary.get(key)

@register.filter
def get_attr(obj, attr):
    """Retorna o valor de um atributo do objeto"""
    if obj:
        return getattr(obj, attr, 0)
    return 0

@register.filter
def percentage(value, total):
    """Calcula a porcentagem de um valor em relação ao total"""
    if total and total > 0:
        return round((value / total) * 100, 1)
    return 0 