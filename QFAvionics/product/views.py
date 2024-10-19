from django.shortcuts import render
from .models import Product
# Create your views here.
def product_view(request):
    product = Product.objects.get(id=1)
    context = {
        "product": product.to_dict()
    }
    context["product"]["images"] = product.images.all()
    # images = product.images.all()[0]
    # print(images[0])
    return render(request, 'product.html', context)

def product_by_category(request):
    return render(request, 'product_by_category.html')