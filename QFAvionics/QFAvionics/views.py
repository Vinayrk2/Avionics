from django.shortcuts import redirect, render
from product.models import Category, Product
from additional_option.models import Service, HomeSection
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from additional_option.models import AboutContent


def home(request):
    categories = Category.objects.all()[:4]
    products = Product.objects.all()[:4]

    whatwedo = HomeSection.objects.filter(pk=1)
    
    if whatwedo:
        whatwedo = whatwedo.first().items.all()
    else:
        whatwedo = []
    
    products_dict = []
    
    for product in products:
        temp = product.to_dict(request)
        temp["image"] = product.get_image().url
        products_dict.append(temp)
        
    return render(request, "home.html", {'categories':categories, 'products':products_dict, 'whatwedo':whatwedo })

def aboutpage(request):
    about = AboutContent.objects.filter(pk=1)
    
    if about:
        about = about.first()
        sections = about.sections.all()
    else:
        sections = []
    return render(request, "about.html", {'content':about, 'sections':sections})

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
