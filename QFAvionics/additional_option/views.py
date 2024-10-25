from django.shortcuts import render
from .models import Service
# Create your views here.
def service(request, id):
    service = Service.objects.filter(id=id).first()
    return render(request, 'service.html', {'service':service})