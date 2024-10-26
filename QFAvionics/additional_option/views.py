from django.shortcuts import render
from .models import Service
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def service(request, id):
    service = Service.objects.filter(id=id).first()
    return render(request, 'service.html', {'service':service})


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

