from django.contrib import admin
from .models import Service, Link
from .models import SiteSettings
from .adminform import ServiceForm

admin.site.register(SiteSettings)

# Register your models here.
@admin.register(Service)
class ProductAdmin(admin.ModelAdmin):
    
    form =  ServiceForm
    
    class Media:
        # \static\js\product_admin.js
        js = ('js/productadmin.js','js/add_tech_info.js')
        css = {
            'all': ('css/index.css',)
        }
admin.site.register(Link)
