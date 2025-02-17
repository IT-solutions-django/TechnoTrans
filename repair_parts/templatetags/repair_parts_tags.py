from django import template
from ..models import (
    RepairPart,
)


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
def repair_part_count_for_category(category_id: int):
    return RepairPart.objects.filter(categories__id=category_id).count()


@register.simple_tag
def repair_part_count_for_brand(brand_id: int):
    return RepairPart.objects.filter(brand_id=brand_id).count()