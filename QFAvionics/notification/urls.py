from django.urls import path
from . import views

urlpatterns = [
    path('',  views.notifications, name='view-news'),
    path('view/<int:id>/',  views.view_details, name='view-perticular-news'),
]
