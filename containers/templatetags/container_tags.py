from django import template


register = template.Library()


@register.filter(name='foot_to_symbol')
def foot_to_symbol(value: str):
    return value.replace(' футов', '’')
