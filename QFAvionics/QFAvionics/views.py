from django.shortcuts import render
from product.models import Category, Product

def home(request):
    categories = Category.objects.all()[:4]
    products = Product.objects.all()[:6]
    services = [{
        "image":"images/warehouse.webp",
        "name": "ONLINE STORE",
        "description":"Use this section to explain a set of product features, to link to a series of pages, or to answer common questions about your products. Add images for emphasis."
    },
    {
     "image":"images/warehouse.webp",
        "name": "EQUIPMENT INSTALLATION",
        "description":"Use this section to explain a set of product features, to link to a series of pages, or to answer common questions about your products. Add images for emphasis."   
    },
    {
     "image":"images/warehouse.webp",
        "name": "SERVICES",
        "description":"We provide a comprehensive range of value-driven helicopter and fixed-wing maintenance, repair and overhaul services"   
    },
    
    {
     "image":"images/warehouse.webp",
        "name": "LINE MAINTENANCE",
        "description":"Use this section to explain a set of product features, to link to a series of pages, or to answer common questions about your products. Add images for emphasis."   
    },
    
    {
     "image":"images/warehouse.webp",
        "name": "RETROFITS",
        "description":"Use this section to explain a set of product features, to link to a series of pages, or to answer common questions about your products. Add images for emphasis"   
    },
    
    {
     "image":"images/warehouse.webp",
        "name": "MAINTENANCE, REPAIR & OVERHAUL (MRO)",
        "description":"We provide best-in-class helicopter and fixed-wing MRO services for several of the most commonly operated light, medium and heavy helicopter models."   
    }
    ]
    products_dict = []
    
    for product in products:
        temp = product.to_dict(request)
        temp["image"] = product.get_image().url
        products_dict.append(temp)
        
    return render(request, "home.html", {'categories':categories, 'products':products_dict, 'comp_services':services})

def aboutpage(request):
    return render(request, "about.html", {})

def contactpage(request):
    return render(request, "contact.html", {})