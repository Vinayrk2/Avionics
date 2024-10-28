from django.contrib import admin
from .models import Service, Link
from .models import SiteSettings

admin.site.register(SiteSettings)

# Register your models here.
admin.site.register(Service)
admin.site.register(Link)
