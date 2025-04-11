from django import template
from ..models import UniversalContainer
from ..views import get_min_and_max_price_for_choice


register = template.Library()


@register.filter(name='foot_to_symbol')
def foot_to_symbol(value: str):
    return value.replace(' футов', '’')


@register.filter(name='applied_filter_name_translate')
def applied_filter_name_translate(value: str):
    mapper = {
        'price': 'Цена', 
        'category': 'Тип', 
        'container_type': 'Размер', 
        'brand': 'Производитель', 
        'year': 'Год выпуска',
    }
    return mapper.get(value, None)


@register.simple_tag
def container_count_for_category(category_id: int):
    return UniversalContainer.objects.filter(categories__id=category_id).count()


@register.simple_tag
def container_count_for_price(price_range: str):
    min_price, max_price = get_min_and_max_price_for_choice(price_range)
    return UniversalContainer.objects.filter(price__gte=min_price, price__lt=max_price).count()


@register.simple_tag
def container_count_for_brand(brand_id: int):
    return UniversalContainer.objects.filter(brand_id=brand_id).count()


@register.simple_tag
def container_count_for_year(year: int):
    return UniversalContainer.objects.filter(year=year).count()


@register.simple_tag
def container_count_for_container_type(container_type: int):
    return UniversalContainer.objects.filter(container_type=container_type).count()