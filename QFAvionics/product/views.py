from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib import messages
from notification.models import Notification

def product_view(request, id):
    product = Product.objects.filter(id=id).first()
    if product:
        context = {
            "product": product.to_dict(request),
            "related_products":product.get_related_products(request)
        }
        context["product"]["images"] = product.images.all()
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

def search_result(request):
    query = request.GET.get("q")
    if query == "":
        messages.add_message(request, messages.WARNING, "Please enter a search query")        
        return redirect("home")
    elif query is None:
        messages.add_message(request, messages.WARNING, "Please enter a search query")        
        return redirect("home")
    elif query:
        product_dict = []
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(part_number__icontains=query) | Product.objects.filter(category__name__icontains=query)
        for product in products:
            pr = product.to_dict(request)
            pr["image"] = product.get_image().url
            product_dict.append(pr)
        news = Notification.objects.filter(title__icontains=query) |  Notification.objects.filter(description__icontains=query)

    return render(request, "search_result.html", {'products':product_dict,  "query":query, 'news':news})
