from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from user.views import signup,userlogin, userlogout

urlpatterns = [
    path("view", views.product_view, name="product-view"),
    
] 