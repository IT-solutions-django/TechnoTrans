from containers.models import (
    Container, 
    Category,
)
from contacts.models import PopularQuestion
from contacts.models import CompanyInfo
from .forms import FeedbackForm


def global_context(request):
    categories = Category.objects.all()
    popular_questions = PopularQuestion.objects.all()
    return {
        'categories': categories,
        'feedback_form': FeedbackForm(),
        'popular_questions': popular_questions,
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