from django.contrib import admin
from .models import Category, Product, Image
from .adminform import ProductForm
from django.utils.html import format_html
from django.templatetags.static import static

class ProductAttributeInline(admin.TabularInline):
    model = Image
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductAttributeInline]
    form =  ProductForm
    
    class Media:
        # \static\js\product_admin.js
        js = ('js/productadmin.js',)

# admin.site.register(Product, ProductAdmin)

admin.site.register([Category])