from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from user.views import signup,userlogin, userlogout

urlpatterns = [
    path("view/<int:id>/", views.product_view, name="product-view"),
    path("category/<str:name>/", views.product_by_category, name="product-list-categorized")
] 