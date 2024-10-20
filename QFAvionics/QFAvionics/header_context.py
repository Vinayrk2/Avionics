from product.models import Category

def header_options(request):
    options = {
        "categories": [category.name for  category in Category.objects.all()],
    }
    
    return {'categories': options}
