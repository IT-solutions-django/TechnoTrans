from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
from containers.services import get_paginated_collection
from containers.views import get_min_and_max_price_for_choices 
from .forms import GeneratorFilterForm
from .models import Generator, GeneratorType, GeneratorPower


class GeneratorsCatalogView(View): 
    template_name = 'generators/generators.html' 

    MAX_INT = 10**10
    ITEMS_PER_PAGE = 12

    def get(self, request): 
        filter_form = GeneratorFilterForm(request.GET)
        generators = Generator.objects.all()

        selected_years = []
        selected_powers = []
        selected_types = []

        if filter_form.is_valid():
            cd = filter_form.cleaned_data

            selected_categories = cd.get('category')
            if selected_categories: 
                generators = generators.filter(categories__id__in=selected_categories)

            if cd.get('category'):
                generators = generators.filter(categories__id__in=cd['category']).distinct()

            if cd.get('generator_type'):
                print(cd.get('generator_type'))
                generators = generators.filter(generator_type_id__in=cd['generator_type']).distinct()
                selected_types = list(GeneratorType.objects.filter(id__in=cd['generator_type']).values_list('name', flat=True))

            if cd.get('power'):
                generators = generators.filter(power__id__in=cd['power']).distinct()
                selected_types = list(GeneratorType.objects.filter(id__in=cd['power']).values_list('name', flat=True))

            if cd.get('year'):
                generators = generators.filter(year__in=cd['year'])
                selected_years = list(map(str, cd['year']))

            if cd.get('price'): 
                min_price, max_price = get_min_and_max_price_for_choices(cd.get('price'))
                print(min_price)
                generators = generators.filter(price__gte=min_price)
                if max_price < self.MAX_INT:
                    generators = generators.filter(price__lt=max_price)


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

            
        generators = get_paginated_collection(request, generators, self.ITEMS_PER_PAGE)

        context = {
            'generators': generators,
            'generators_count': generators.object_list.count(),
            'filter_form': filter_form,
            'applied_filters': applied_filters,
            'selected_years': ', '.join(selected_years),
            'selected_powers': ', '.join(selected_powers),
            'selected_types': ', '.join(selected_types),
        }
        return render(request, self.template_name, context)
    

class GeneratorView(View): 
    template_name = 'generators/generator.html' 

    def get(self, request, generator_slug: str): 
        generator = get_object_or_404(Generator, slug=generator_slug)
        context = {
            'generator': generator,
        }
        return render(request, self.template_name, context)
    

class GeneratorsRentView(View): 
    template_name = 'generators/rent.html' 

    def get(self, request): 
        context = {
            'generator': 'generator',
        }
        return render(request, self.template_name, context)