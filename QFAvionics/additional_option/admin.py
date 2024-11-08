from django.contrib import admin
from .models import Service, Link
from .models import SiteSettings, AboutSection, AboutContent, HomeSection
from .adminform import ServiceForm, AboutSectionForm
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import HomeSection, HomeSectionItem, CarasoleImage

admin.site.register(SiteSettings)

# Register your models here.
@admin.register(Service)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')
    form =  ServiceForm
    
    class Media:
        # \static\js\product_admin.js
        js = ('js/productadmin.js','js/add_tech_info.js')
        css = {
            'all': ('css/admin.css',)
        }
        

admin.site.register(AboutContent)
        
@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    form = AboutSectionForm
    
    class Media:
        # \static\js\product_admin.js
        js = ('js/about_section.js',)
        css = {
            'all': ('css/admin.css',)
        }
        
admin.site.register(Link)

class HomeSectionItemInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if len(self.forms) > 6:
            raise ValidationError("You can only add up to 6 items for the Home Section.")
        
# class CarasolImageSet(admin.ModelAdmin):
    

class HomeSectionItemInline(admin.TabularInline):
    model = HomeSectionItem
    formset = HomeSectionItemInlineFormset
    extra = 1
    max_num = 6 
    
    
class HomeSectionImageInline(admin.TabularInline):
    model = CarasoleImage
    extra = 1
    max_num = 3


@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    inlines = [HomeSectionItemInline, HomeSectionImageInline]
