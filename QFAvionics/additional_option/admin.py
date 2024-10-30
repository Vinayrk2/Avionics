from django.contrib import admin
from .models import Service, Link
from .models import SiteSettings, AboutSection, AboutContent
from .adminform import ServiceForm, AboutSectionForm

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
        

admin.site.register(AboutContent)
        
@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    form = AboutSectionForm
    
    class Media:
        # \static\js\product_admin.js
        js = ('js/about_section.js',)
        css = {
            'all': ('css/index.css',)
        }
        
admin.site.register(Link)
# admin.site.register(AboutSection)
