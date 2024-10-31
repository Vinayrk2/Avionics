from django.contrib import admin
from django.urls import path, include
from .views import home, aboutpage, contactpage, service
from django.conf import settings
from django.conf.urls.static import static
from user.views import signup,userlogin, userlogout, userprofile, verify_email
from additional_option.views import service, set_currency
from django.contrib.auth import views as auth_views

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
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
