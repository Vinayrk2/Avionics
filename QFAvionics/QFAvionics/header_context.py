from shopcart.views import get_total_items
from product.models import Category
from additional_option.models import Service, Link
from cart.cart import Cart

def header_options(request):

    options = {
        "categories": [category.name for category in Category.objects.all()],
        "services" : [service for service in Service.objects.all()],
        "links": Link.objects.all(),
        "no_of_items":  get_total_items(request),
    }
    
    return options
