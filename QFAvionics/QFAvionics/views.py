from django.shortcuts import redirect, render
from product.models import Category, Product
from additional_option.models import Service
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def home(request):
    categories = Category.objects.all()[:4]
    products = Product.objects.all()[:4]
    services = [{
        "image":"images/warehouse.webp",
        "name": "ONLINE STORE",
        "description":"We provide several online services such as viewing our products, receiving news on business etc."
    },
    {
     "image":"images/warehouse.webp",
        "name": "EQUIPMENT INSTALLATION",
        "description":"Equipment Installation means any actions that are necessary to attach the equipment to the building including, but not limited to bolting or welding.."   
    },
    {
     "image":"images/warehouse.webp",
        "name": "SERVICES",
        "description":"We provide a comprehensive range of value-driven helicopter and fixed-wing maintenance, repair and overhaul services"   
    },
    
    {
     "image":"images/warehouse.webp",
        "name": "LINE MAINTENANCE",
        "description":"Line maintenance is the routine and preventive maintenance that is performed on an aircraft before, between, or after flights. It includes tasks such as checking the oil levels, tire pressures etc."   
    },
    
    {
     "image":"images/warehouse.webp",
        "name": "RETROFITS",
        "description":"A retrofit is the process of adding new or modified parts or equipment to something that was previously constructed or manufactured. Retrofits can be done for a variety of reasons, for improve energy efficiency."   
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
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('description')
        subject = request.POST.get("subject")
        
        html_message = render_to_string('emailcomplaint.html', {
            'name': name,
            'email': email,
            'message': message,
            'subject': subject
        })
        flag = send_mail(
            subject=subject,
            message=message, 
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            html_message=html_message,
            fail_silently=False,
        )
        if flag:
            messages.success(request, "Your message has been sent successfully!")
            return redirect("/")
        else:
            messages.add_message(request,  messages.ERROR, 'Failed to send mail, try again later')
            return redirect("/")
        
    # else:
    #     messages.add_message(request,  messages.INFO, 'Invalid Operation')
    #     return redirect("/")
    else:
        return render(request, "contact.html", {})

def service(request, servicename):
    service_perticular = Service.objects.filter(name=servicename).first()
    if service_perticular:
        return render(request, "service.html", {'service':service_perticular})
    else:
        messages.add_message(request,  messages.INFO, 'Service not found')
        return redirect("home")
