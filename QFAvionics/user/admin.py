from django.contrib import admin
from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login', 'password')
    list_filter = ('is_active', 'is_staff')
    ordering = ('-date_joined',)