from django.shortcuts import render
from django.views import View 
from django.http import JsonResponse
from containers.models import (
    Brand, 
    Category, 
    Container, 
    ContainerType,
)
from django.urls import reverse
from contacts.models import Partner
from loguru import logger
from .forms import FeedbackForm, CalculatePriceRequestForm
from .models import CalculatePriceRequest, Request 
from .services import send_email


class HomeView(View): 
    template_name = 'home/home.html'

    def get(self, request): 
        categories = Category.objects.all().prefetch_related('category_containers').all()
        calculate_form = CalculatePriceRequestForm()
        brands_list = ', '.join(brand.name for brand in Brand.objects.all())
        partners = Partner.objects.all()
        brand_names = ('Carrier', 'Thermo King', 'Star Cool', 'Daikin')
        urls_filtered_by_brand = {
            brand.replace(' ', ''): f"{reverse('containers:catalog')}?brand={Brand.objects.filter(name=brand).first().pk}"
            for brand in brand_names
        }
        context = {
            'categories': categories,
            'calculate_form': calculate_form,
            'brands_list': brands_list,
            'partners': partners,
            'urls_filtered_by_brand': urls_filtered_by_brand,
        }
        return render(request, self.template_name, context)
    

class SaveRequestView(View): 
    def post(self, request): 
        form: FeedbackForm = FeedbackForm(request.POST) 
        if form.is_valid():
            try: 
                new_request: Request = form.save() 
                
                email_subject = f'Новая заявка с сайта' 
                email_message = f'Имя: {new_request.name}\nТелефон: {new_request.phone}' 
                if new_request.message: 
                    email_message += f'\nСообщение: {new_request.message}'
                send_email(
                    subject=email_subject, 
                    content=email_message
                )

            except Exception as e: 
                logger.error('Ошибка при сохранении заявки')

            return JsonResponse({'status': 'ok'}, status=200)
        print(form.errors)
        return JsonResponse({'status': 'error'}, status=400)
    

class SaveCalculateRequestView(View): 
    def post(self, request): 
        form = CalculatePriceRequestForm(request.POST) 
        if form.is_valid():
            try: 
                service_type = form.cleaned_data.pop("service_type")
                new_request: CalculatePriceRequest  = form.save() 

                email_subject = f'Новая заявка с сайта (расчёт стоимости обслуживания)' 
                email_message = f'Тип контейнера: {new_request.container_type}\nВид обслуживания: {new_request.service_type}\nГород: {new_request.city}\nТелефон: {new_request.phone}' 
                if new_request.message: 
                    email_message += f'\nСообщение: {new_request.message}'
                send_email(
                    subject=email_subject, 
                    content=email_message
                )

                logger.info(f"Заявка сохранена: {new_request}, Вид обслуживания: {service_type}")

                return JsonResponse({"status": "ok"}, status=200)
            except Exception as e: 
                logger.error(f"Ошибка при сохранении заявки: {e}")
                return JsonResponse({"status": "error"}, status=500)

        return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    

class Test404View(View): 
    template_name = '404.html' 

    def get(self, request): 
        return render(request, self.template_name)
    

def handler404(request, *args, **argv):
    return render(request, '404.html', status=404)