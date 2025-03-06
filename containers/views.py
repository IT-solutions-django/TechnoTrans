from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View 
from django.db.models import Min
from .models import Container, ContainerType, Brand, ContainerImage
from .forms import FilterForm
from django.core.files.temp import NamedTemporaryFile
from .services import get_paginated_collection
from django.core.files import File



class CatalogView(View): 
    template_name = 'containers/catalog.html' 

    MAX_INT = 10**10
    ITEMS_PER_PAGE = 12

    def get(self, request): 
        containers = Container.objects.all() 
        filter_form = FilterForm(request.GET)
        min_price = Container.objects.aggregate(Min('price'))['price__min']

        selected_years = []
        selected_brands = []
        selected_types = []

        if filter_form.is_valid():
            cd = filter_form.cleaned_data

            selected_categories = cd.get('category')
            if selected_categories: 
                containers = containers.filter(categories__id__in=selected_categories)

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
    

class AddContainersView(View): 
    def get(self, request): 
        import requests 
        from bs4 import BeautifulSoup

        response = requests.get('https://refexpress.ru/prodazha-refkonteynerov/')

        with open('file.html', 'w', encoding='utf-8') as file: 
            file.write(response.text)

        if response.status_code == 200:
            # Создаем объект BeautifulSoup для парсинга
            soup = BeautifulSoup(response.text, 'lxml')
            
            containers = soup.find_all(class_='uc_post_grid_style_one_item')

            for card in containers: 
                link_to_card = card.find(class_='uc_post_grid_style_one_image')['href']
                name = card.find(class_='uc_title').text
                price = int(str(card.find(class_='woocommerce-Price-amount').text).replace('\xa0₽', '').replace(' ', '')[:-3])

                response = requests.get(link_to_card) 

                container, created = Container.objects.get_or_create(
                    name=name,
                    defaults={
                        'price': price,
                        'slug': generate_slug(name)
                    }
                )
                container.save()


                soup = BeautifulSoup(response.text, 'lxml') 
                images = soup.find_all(class_='woocommerce-product-gallery__image')


                container.images.all().delete()
                for img in images:
                    image_url = img.find("a").find("img")["data-large_image"]
                    image_name = image_url.split('/')[-1] 

                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        img_temp = NamedTemporaryFile()
                        img_temp.write(image_response.content)
                        img_temp.flush()

                        container_image = ContainerImage(container=container)
                        container_image.image.save(image_name, File(img_temp))

                        print(f'Сохранено изображение: {image_name} для контейнера {container}')

            
        return JsonResponse({'status': 'super'})


def generate_slug(name: str) -> str:
    import re
    from transliterate import translit
    """
    Генерирует слаг из названия.
    Транслитерирует русские символы в латиницу, убирает пробелы и специальные символы.
    """
    slug = translit(name, 'ru', reversed=True)
    
    slug = re.sub(r'[^a-zA-Z0-9-]', ' ', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = slug.lower().strip('-') 
    
    return slug