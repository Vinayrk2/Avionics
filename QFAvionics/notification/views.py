from django.shortcuts import render, redirect
from .models import Notification
from django.contrib import messages

def notifications(request):
    notifications = Notification.objects.all()[:10]
    return render(request, 'notifications.html', {'notifications':notifications})

def view_details(request, id):
    notification = Notification.objects.filter(id=id).first()
    if notification:
        return render(request, 'notification_details.html', {'notification':notification})
    else:
        messages.info(request, "News has been removed.")
        return redirect("home")
    # return render(request, 'notification_details.html', {'notification':notification})