"""
Filtros personalizados para templates de Django
"""
from django import template

register = template.Library()


@register.filter
def mul(value, arg):
    """
    Multiplica el valor por el argumento.
    Uso: {{ forloop.counter0|mul:0.1 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
