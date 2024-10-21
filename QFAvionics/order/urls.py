from django.urls import path
from . import views

urlpatterns = [
    path('payment/create/', views.create_payment, name='create_payment'),
    path('payment/execute/', views.execute_payment, name='execute_payment'),
]
