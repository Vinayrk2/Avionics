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
    search_fields = ('name', 'part_number')
    list_filter = ('category', 'stock_quantity')
    list_display = ('name', 'category', 'price', 'stock_quantity', 'created_at')
    
    
    class Media:
        js = ('js/productadmin.js',)
        css = {
            'all': ('css/admin.css',)
        }
        
# admin.site.register(Product, ProductAdmin)

admin.site.register([Category])