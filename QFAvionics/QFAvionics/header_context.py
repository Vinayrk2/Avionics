from product.models import Category
from additional_option.models import Service

def header_options(request):
    options = {
        "categories": [category.name for category in Category.objects.all()],
        "services" : [service.name for service in Service.objects.all()]
    }
    
    return options
