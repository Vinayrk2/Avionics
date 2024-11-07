from shopcart.views import get_total_items
from product.models import Category
from additional_option.models import Service, Link
from cart.cart import Cart
from additional_option.models import SiteSettings

def header_options(request):

    location = SiteSettings.objects.filter(pk=1)
    if location is not None:
        location = location.first()

    options = {
        "categories": [category.name for category in Category.objects.all()],
        "services" : [service for service in Service.objects.all()],
        "links": Link.objects.all(),
        "no_of_items":  get_total_items(request),
        "footer": location.get_footer_data(),
        "header": location.get_header_data,
    }
    
    return options
