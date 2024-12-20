from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib import messages
from notification.models import News
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product


def get_filtered_products(request, category=''):
    # Get filter parameters from the request
    category_id = request.GET.getlist('category')
    manufacturer = request.GET.getlist('manufacturer')
    condition = request.GET.getlist('condition')
    availability = request.GET.getlist('availability')
    # Build a query dynamically
    filters = Q()
    if category_id:
        filters &= Q(category_id__in=category_id)
    if manufacturer:
        filters &= Q(manufacturer__in=manufacturer)
    if availability:
        filters &= Q(availability__in=availability)
    if condition:
        filters &= Q(condition__in=condition)
    if category != 'all' and category != '':
        filters &= Q(category__name=category)

    # Apply filters to the Product model
    filtered_products = Product.objects.filter(filters).distinct()
    
    return filtered_products

def get_filter_options():
    # get the distinct values for each filter option
    categories = Category.objects.all()
    manufacturers = Product.objects.values('manufacturer').distinct()
    conditions = Product.objects.values('condition').distinct()
    availabilities = Product.objects.values('availability').distinct()
    
    return {
        'categories': categories,
        'manufacturers': manufacturers,
        'conditions': conditions,
        'availabilities': availabilities
    }

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
    # try:
        # if  name == "all":
        #     products = Product.objects.all()
        # else:
        #     category = Category.objects.get(name=name)
        #     products = Product.objects.filter(category__name=category.name)
    # except Exception as e:
    #     messages.add_message(request,  messages.WARNING, "Sorry! The category is not available")        
    #     return redirect("/")
    # if name != "all":
    #     if request.GET.get('category'):
    #         data = request.GET.
    if name != "all" and request.GET.get("category",None):
        data = request.GET.dict()
        query = "&".join([f"{key}={value}" for key, value in data.items() if value != ""])
        return redirect(f"/product/category/all/?{query}")
    else:
        products = get_filtered_products(request, category=name)
    products_dict = []
    
    if not products:
        page_obj = None
        filter = get_filter_options()
        return render(request, 'product_by_category.html',{"products":page_obj, 'filters':filter})
    
    for product in products:
        temp = product.to_dict(request)
        temp["image"] = product.get_image().url
        products_dict.append(temp)
        
        paginator = Paginator(products_dict, 15)
        pagenumber = request.GET.get('page',1)
        page_obj = paginator.get_page(pagenumber)
    
    count = {
        'products':  len(products_dict),
    }
    
    filter = get_filter_options()
    return render(request, 'product_by_category.html',{"products":page_obj, "name":name, 'count':count, 'filters':filter})

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
        products = get_filtered_products(request)
        products = products.filter(name__icontains=query) | products.filter(part_number__icontains=query) | products.filter(category__name__icontains=query) | products.filter(manufacturer__icontains=query)
        for product in products:
            pr = product.to_dict(request)
            pr["image"] = product.get_image().url
            product_dict.append(pr)
        if request.GET.get('page') == '1':
            news = News.objects.filter(title__icontains=query) |  News.objects.filter(description__icontains=query)
        else:
            news = None
        paginator = Paginator(product_dict, 15)
        pagenumber = request.GET.get('page',1)
        page_obj = paginator.get_page(pagenumber)
        
    count = {
        'products':  len(product_dict),
    }
    filter = get_filter_options()
    return render(request, "search_result.html", {'products':page_obj,  "query":query, 'news':news, 'count':count, 'filters':filter})
