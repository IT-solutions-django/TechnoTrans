from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from containers.models import Container
from generators.models import Generator 
from universal_containers.models import UniversalContainer


class Site: 
    domain = 'ttrans.pro' 


class BaseSitemap(Sitemap):
    protocol = 'https' 
    
    def get_urls(self, site=None, **kwargs):
        site = Site()
        return super(BaseSitemap, self).get_urls(site=site, **kwargs)
    

class HomeViewSitemap(BaseSitemap): 
    priority = 1 

    def items(self): 
        return [
            'home:home',
        ]
    
    def location(self, item):
        return reverse(item)
    

class StaticViewSitemap(BaseSitemap):
    priority = 0.9

    def items(self):
        return [ 
            'containers:catalog',
            'universal_containers:catalog', 
            'generators:catalog',
            'containers:rent',
            'generators:rent',
            'contacts:about_company', 
            'contacts:cargo_transportation', 
            'contacts:documentation',
            'contacts:contacts',
        ]  

    def location(self, item):
        return reverse(item)
    

class ContainerViewSitemap(BaseSitemap): 
    priority = 0.8 

    def items(self): 
        return Container.objects.all()
    

class GeneratorViewSitemap(BaseSitemap): 
    priority = 0.7 

    def items(self): 
        return Generator.objects.all()
    

class UnversalContainerViewSitemap(BaseSitemap): 
    priority = 0.7 

    def items(self): 
        return UniversalContainer.objects.all()