from django import template
from django.utils.safestring import mark_safe 
import markdown 


register = template.Library()


@register.filter(name='price_format')
def price_format(value: str):
    try:
        value = int(value)
        return f"{value:,}".replace(',', ' ')
    except (ValueError, TypeError):
        return value 


@register.filter(name='markdown')
def markdown_format(text: str): 
    return mark_safe(markdown.markdown(text))