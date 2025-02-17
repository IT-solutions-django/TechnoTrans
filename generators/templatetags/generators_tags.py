from django import template
from containers.views import get_min_and_max_price_for_choice
from ..models import Generator


register = template.Library()


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
def generator_count_for_category(category_id: int):
    return Generator.objects.filter(categories__id=category_id).count()


@register.simple_tag
def generator_count_for_type(type_id: int):
    return Generator.objects.filter(generator_type__id=type_id).count()


@register.simple_tag
def generator_count_for_price(price_range: str):
    min_price, max_price = get_min_and_max_price_for_choice(price_range)
    return Generator.objects.filter(price__gte=min_price, price__lt=max_price).count()


@register.simple_tag
def generator_count_for_year(year: int):
    return Generator.objects.filter(year=year).count()


@register.simple_tag
def generator_count_for_power(power_id: int):
    return Generator.objects.filter(power__id=power_id).count()