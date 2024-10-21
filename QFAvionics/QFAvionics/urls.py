from django.contrib import admin
from django.urls import path, include
from .views import home
from django.conf import settings
from django.conf.urls.static import static
from user.views import signup,userlogin, userlogout, userprofile

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("signup/", signup, name="signup"),
    path("login/", userlogin, name="login"),
    path("logout", userlogout, name="logout"),
    path("user/profile", userprofile, name="profile"),
    path("product/", include("product.urls")),
    path("cart/", include("shopcart.urls")),
    path("order/", include("order.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)