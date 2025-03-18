from containers.models import (
    Container, 
    Category,
)
from contacts.models import PopularQuestion, CityInfo
from contacts.models import CompanyInfo
from .forms import FeedbackForm


def global_context(request):
    categories = Category.objects.all()
    rent_category = Category.objects.all().filter(name__icontains='Аренда').first()
    popular_questions = PopularQuestion.objects.all()
    filials = CityInfo.objects.all()
    return {
        'categories': categories,
        'feedback_form': FeedbackForm(),
        'popular_questions': popular_questions,
        'rent_category': rent_category,
        'filials': filials,
    }


def company_info(request):
    try:
        info = CompanyInfo.get_instance()
    except CompanyInfo.DoesNotExist:
        info = None

    context = {
        'company_info': info,
    }

    return context