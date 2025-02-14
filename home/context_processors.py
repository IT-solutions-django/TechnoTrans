from containers.models import (
    Container, 
    Category,
)


def global_context(request):
    categories = Category.objects.all()
    return {
        'categories': categories,
    }
