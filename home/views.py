from django.shortcuts import render
from django.views import View 
from django.http import JsonResponse
from containers.models import (
    Brand, 
    Category, 
    Container, 
    ContainerType,
)
from contacts.models import Partner
from loguru import logger
from .forms import FeedbackForm, CalculatePriceRequestForm
from .models import Request 


class HomeView(View): 
    template_name = 'home/home.html'

    def get(self, request): 
        categories = Category.objects.all().prefetch_related('category_containers').all()
        calculate_form = CalculatePriceRequestForm()
        brands_list = ', '.join(brand.name for brand in Brand.objects.all())
        partners = Partner.objects.all()
        context = {
            'categories': categories,
            'calculate_form': calculate_form,
            'brands_list': brands_list,
            'partners': partners,
        }
        return render(request, self.template_name, context)
    

class SaveRequestView(View): 
    def post(self, request): 
        form: FeedbackForm = FeedbackForm(request.POST) 
        if form.is_valid():
            try: 
                new_request: Request = form.save() 
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
                new_request = form.save() 

                logger.info(f"Заявка сохранена: {new_request}, Вид обслуживания: {service_type}")

                return JsonResponse({"status": "ok"}, status=200)
            except Exception as e: 
                logger.error(f"Ошибка при сохранении заявки: {e}")
                return JsonResponse({"status": "error"}, status=500)

        return JsonResponse({"status": "error", "errors": form.errors}, status=400)