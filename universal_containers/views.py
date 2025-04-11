from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View 
from django.db.models import Min
from .models import UniversalContainer, ContainerType, Brand, UniversalContainerImage, Category
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from .forms import FilterForm
from containers.services import get_paginated_collection



class UniversalCatalogView(View): 
    template_name = 'universal_containers/catalog.html' 

    MAX_INT = 10**10
    ITEMS_PER_PAGE = 12

    def get(self, request): 
        containers = UniversalContainer.objects.all() 
        filter_form = FilterForm(request.GET)
        min_price = UniversalContainer.objects.aggregate(Min('price'))['price__min']

        selected_years = []
        selected_brands = []
        selected_types = []
        selected_category = None

        if filter_form.is_valid():
            cd = filter_form.cleaned_data

            selected_categories = cd.get('category')
            if selected_categories: 
                containers = containers.filter(categories__id__in=selected_categories)\
                
            if len(selected_categories) == 1: 
                [category_id] = selected_categories
                selected_category = Category.objects.get(id=category_id)

            if cd.get('category'):
                containers = containers.filter(categories__id__in=cd['category']).distinct()

            if cd.get('container_type'):
                containers = containers.filter(container_type__id__in=cd['container_type'])
                selected_types = list(ContainerType.objects.filter(id__in=cd['container_type']).values_list('name', flat=True))

            if cd.get('brand'):
                containers = containers.filter(brand__id__in=cd['brand'])
                selected_brands = list(Brand.objects.filter(id__in=cd['brand']).values_list('name', flat=True))

            if cd.get('year'):
                containers = containers.filter(year__in=cd['year'])
                selected_years = list(map(str, cd['year']))

            if cd.get('price'): 
                min_price, max_price = get_min_and_max_price_for_choices(cd.get('price'))
                containers = containers.filter(price__gte=min_price)
                if max_price < self.MAX_INT:
                    containers = containers.filter(price__lt=max_price)


        applied_filters = []
        for field_name, field in filter_form.fields.items():
            values = request.GET.getlist(field_name) 
            if values:
                for value in values:
                    try:
                        value = int(value)
                    except ValueError:
                        pass  

                    applied_filters.append({
                        'name': field.label or field_name,
                        'value': value,
                        'human_value': dict(field.choices).get(value, value)
                    })
            
        containers = get_paginated_collection(request, containers, self.ITEMS_PER_PAGE)

        brands_list = ', '.join(brand.name for brand in Brand.objects.all())

        context = {
            'containers': containers,
            'filter_form': filter_form,
            'applied_filters': applied_filters,
            'selected_years': ', '.join(selected_years),
            'selected_brands': ', '.join(selected_brands),
            'selected_types': ', '.join(selected_types),
            'min_price': min_price,
            'brands_list': brands_list,
            'selected_category': selected_category,
        }
        return render(request, self.template_name, context)
    

class UniversalContainerView(View): 
    template_name = 'universal_containers/container.html'

    def get(self, request, container_slug: int): 
        container = get_object_or_404(UniversalContainer, slug=container_slug)
        container.is_new = container.categories.all().filter(name='Новые').exists()
        context = {
            'container': container,
        }
        return render(request, self.template_name, context)
    

def get_min_and_max_price_for_choices(price_range_choices: list) -> tuple[float, float]: 
    min_price = UniversalCatalogView.MAX_INT
    max_price = 0
    for price_range in price_range_choices: 
        print(price_range.split('-'))
        min_price_curr, max_price_curr = price_range.split('-')

        if not max_price_curr or max_price_curr == '': 
            max_price_curr = UniversalCatalogView.MAX_INT

        min_price = min(min_price, float(min_price_curr))
        max_price = max(max_price, float(max_price_curr))

    print(int(min_price), int(max_price))
    return int(min_price), int(max_price)


def get_min_and_max_price_for_choice(price_range_choice: str) -> tuple[float, float]: 
    min_price = UniversalCatalogView.MAX_INT
    max_price = 0
    min_price_curr, max_price_curr = price_range_choice.split('-')

    if not max_price_curr or max_price_curr == '': 
        max_price_curr = UniversalCatalogView.MAX_INT

    min_price = min(min_price, int(min_price_curr))
    max_price = max(max_price, int(max_price_curr))

    return int(min_price), int(max_price)