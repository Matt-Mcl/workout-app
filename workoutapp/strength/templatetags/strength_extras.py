from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def diff(value, arg):
    
    if value == '-' or arg == '-':
        return ""
    
    change = float(value) - float(arg)

    if change == 0:
        return ""

    return Decimal(change).normalize()
