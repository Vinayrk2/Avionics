from django.shortcuts import render, redirect
from .models import Service, GalleryItem, GalleryItemDetail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from cart.cart import Cart
from django.contrib import messages

def galary_list(request):
    items = GalleryItem.objects.all()
    return render(request, 'galary_view.html', {'items': items})

def galary_detail(request, pk):
    try:
        item = GalleryItem.objects.filter(pk=pk).first()
        subitems = item.subitems.all()
        
        gallery = GalleryItem.objects.get(id=1)
        print(gallery.heading)

        # Fetch all associated images and descriptions
        for image in gallery.subitems.all():
            print(image.description, image.image.url)
        print(subitems)
        return render(request, 'galary_item.html', {'item': item, 'subitems':subitems})
    except GalleryItem.DoesNotExist as e:
        return render(request, '404.html', {"error":e})

def service(request, id):
    service = Service.objects.filter(id=id).first()
    if service:
        return render(request, 'service.html', {'service':service})
    else:
        messages.add_message(request, messages.INFO, 'Service not found')
        return redirect('home')


@csrf_exempt  # Disable CSRF for simplicity; use CSRF tokens in production
def set_currency(request):
    if request.method == "POST":
        try:
            # Load the JSON data from the request body
            data = json.loads(request.body)
            currency = data.get("currency")

            print("Received currency:", currency)  # Debugging output

            if currency in ["USD", "CAD"]:
                request.session["currency"] = currency
                return JsonResponse({"success": True, "currency": currency})
            else:
                return JsonResponse({"success": False, "error": "Invalid currency"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

