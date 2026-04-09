from django import template

register = template.Library()


@register.filter
def has_group(user, group_name):
    """
    Retorna True se o usuário autenticado pertencer ao grupo informado.
    Uso no template: {% if user|has_group:"bi" %} ... {% endif %}
    """
    if not getattr(user, "is_authenticated", False):
        return False
    return user.groups.filter(name=group_name).exists()


