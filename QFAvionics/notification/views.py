from django.shortcuts import render, redirect
from .models import News
from django.contrib import messages
from django.core.paginator import Paginator

def notifications(request):
    notifications = News.objects.all().order_by('-created_at')[:10]

    paginator = Paginator(notifications, 12)
    pagenumber = request.GET.get('page',1)
    page_obj = paginator.get_page(pagenumber)

    count = {
        "notifications": notifications.count()
    }
    return render(request, 'notifications.html', {'notifications':page_obj, 'count':count})
