from django.shortcuts import render
from django.views import View 
from containers.models import (
    Brand, 
    Category, 
    Container, 
    ContainerType,

)


class HomeView(View): 
    template_name = 'home/home.html'

    def get(self, request): 

        context = {
            'categories': Category.objects.all().prefetch_related('category_containers').all(),
        }
        return render(request, self.template_name, context)