from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View 
from .models import Container
from .forms import FilterForm
from .services import get_paginated_collection


class CatalogView(View): 
    template_name = 'containers/catalog.html' 

    MAX_INT = 10**10
    ITEMS_PER_PAGE = 12

    def get(self, request): 
        containers = Container.objects.all() 
        filter_form = FilterForm(request.GET)

        if filter_form.is_valid():
            cd = filter_form.cleaned_data

            selected_categories = cd.get('category')
            if selected_categories: 
                containers = containers.filter(categories__id__in=selected_categories)

            if cd.get('category'):
                containers = containers.filter(categories__id__in=cd['category']).distinct()

            if cd.get('container_type'):
                containers = containers.filter(container_type__id__in=cd['container_type'])

            if cd.get('brand'):
                containers = containers.filter(brand__id__in=cd['brand'])

            if cd.get('year'):
                containers = containers.filter(year__in=cd['year'])

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

        context = {
            'containers': containers,
            'filter_form': filter_form,
            'applied_filters': applied_filters,
        }
        return render(request, self.template_name, context)
    

class ContainerView(View): 
    template_name = 'containers/container.html'

    def get(self, request, container_slug: int): 
        container = get_object_or_404(Container, slug=container_slug)
        context = {
            'container': container,
        }
        return render(request, self.template_name, context)
    

def get_min_and_max_price_for_choices(price_range_choices: list) -> tuple[float, float]: 
    min_price = CatalogView.MAX_INT
    max_price = 0
    for price_range in price_range_choices: 
        print(price_range.split('-'))
        min_price_curr, max_price_curr = price_range.split('-')

        if not max_price_curr or max_price_curr == '': 
            max_price_curr = CatalogView.MAX_INT

        min_price = min(min_price, float(min_price_curr))
        max_price = max(max_price, float(max_price_curr))

    print(int(min_price), int(max_price))
    return int(min_price), int(max_price)


def get_min_and_max_price_for_choice(price_range_choice: str) -> tuple[float, float]: 
    min_price = CatalogView.MAX_INT
    max_price = 0
    min_price_curr, max_price_curr = price_range_choice.split('-')

    if not max_price_curr or max_price_curr == '': 
        max_price_curr = CatalogView.MAX_INT

    min_price = min(min_price, int(min_price_curr))
    max_price = max(max_price, int(max_price_curr))

    return int(min_price), int(max_price)
    
    
class ContainersRentView(View): 
    template_name = 'containers/rent.html'

    def get(self, request): 
        context = {

        }
        return render(request, self.template_name, context)