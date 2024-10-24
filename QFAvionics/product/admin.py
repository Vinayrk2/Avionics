from django.contrib import admin
from .models import Category, Product, Image

class ProductAttributeInline(admin.TabularInline):
    model = Image
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductAttributeInline]

admin.site.register(Product, ProductAdmin)

admin.site.register([Category])