from django.shortcuts import render
from django.views import View 
from .models import Container


class CatalogView(View): 
    template_name = 'containers/catalog.html' 

    def get(self, request): 
        containers = Container.objects.all() 

        context = {
            'containers': containers,
        }
        return render(request, self.template_name, context)