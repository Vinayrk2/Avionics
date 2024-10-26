from django.contrib import admin
from django.urls import path, include
from .views import home, aboutpage, contactpage, service
from django.conf import settings
from django.conf.urls.static import static
from user.views import signup,userlogin, userlogout, userprofile
from additional_option.views import service, set_currency

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("signup/", signup, name="signup"),
    path("login/", userlogin, name="login"),
    path("logout/", userlogout, name="logout"),
    path("about/", aboutpage, name="aboutpage"),
    path("contact/", contactpage, name="contactpage"),
    path("user/profile/", userprofile, name="profile"),
    path("product/", include("product.urls")),
    path("cart/", include("shopcart.urls")),
    path("notificaiton/", include("notification.urls")),
    path("service/<int:id>/", service, name="service"),
    path("set_currency/", set_currency, name="set_currency"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)