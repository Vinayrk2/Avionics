from django.shortcuts import render
from .models import Product, Category

def product_view(request, id):
    product = Product.objects.get(id=id)
    context = {
        "product": product.to_dict()
    }
    context["product"]["images"] = product.images.all()
    context["product"]["image"] = product.get_image()
    return render(request, 'product.html', context)

def product_by_category(request,name):
    if  name == "all":
        products = Product.objects.all()
    else:
        category = Category.objects.get(name=name)
        products = Product.objects.filter(category__name=category.name)

    products_dict = []
    categories = Category.objects.all()
    
    for product in products:
        temp = product.to_dict()
        if len(product.images) > 0:
            temp["image"] = product.images.all()[0].image.url
        products_dict.append(temp)
            
    return render(request, 'product_by_category.html',{"products":products_dict, "name":name, "categories":categories})