from django.shortcuts import render
from django.views import View 
from django.shortcuts import get_object_or_404
from .models import (
    RepairPart,
)
from .forms import RepairPartFilterForm
from containers.services import get_paginated_collection


class RepairPartsCatalogView(View): 
    template_name = 'repair_parts/repair_parts.html' 
    MAX_INT = 10**10
    ITEMS_PER_PAGE = 12

    def get(self, request): 
        repair_parts = RepairPart.objects.all()
        filter_form = RepairPartFilterForm(request.GET)

        if filter_form.is_valid():
            cd = filter_form.cleaned_data

            if cd.get('category'):
                repair_parts = repair_parts.filter(categories__id__in=cd['category']).distinct()

            if cd.get('brand'):
                repair_parts = repair_parts.filter(brand__id__in=cd['brand'])


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

        repair_parts = get_paginated_collection(request, repair_parts, self.ITEMS_PER_PAGE)

        context = {
            'repair_parts': repair_parts,
            'filter_form': filter_form,
            'applied_filters': applied_filters,
        }

        return render(request, self.template_name, context)
    

class RepairPartView(View): 
    template_name = 'repair_parts/repair_part.html' 

    def get(self, request, part_slug: str): 
        repair_part = get_object_or_404(RepairPart, slug=part_slug) 

        context = {
            'repair_part': repair_part,
        }

        return render(request, self.template_name, context)