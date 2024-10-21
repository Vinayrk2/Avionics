from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_payment, name='create_payment'),
    path('execute/', views.execute_payment, name='execute_payment'),
    path("confirm/", views.confirm_order, name="order_confirm")
]
