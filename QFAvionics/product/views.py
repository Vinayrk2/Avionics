from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib import messages

def product_view(request, id):
    product = Product.objects.filter(id=id).first()
    if product:
        context = {
            "product": product.to_dict(request)
        }
        context["product"]["images"] = product.images.all()
        context["product"]["image"] = product.get_image()
        return render(request, 'product.html', context)
    else:
        messages.add_message(request, messages.WARNING, "Sorry! The product is not available")        
        return redirect("/")

def product_by_category(request,name):
    try:
        if  name == "all":
            products = Product.objects.all()
        else:
            category = Category.objects.get(name=name)
            products = Product.objects.filter(category__name=category.name)
    except Exception as e:
        messages.add_message(request,  messages.WARNING, "Sorry! The category is not available")        
        return redirect("/")
    products_dict = []
    
    for product in products:
        temp = product.to_dict(request)
        temp["image"] = product.get_image().url
        products_dict.append(temp)
            
    return render(request, 'product_by_category.html',{"products":products_dict, "name":name})