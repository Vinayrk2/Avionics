from django.contrib import admin
from .models import Order
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    # List the fields you want to make read-only
    readonly_fields = ('user','order_date','amount_summary','payment_status','transaction_id','order_id','payer_id','items')

    # Optionally, define which fields to show in the form
    # fields = ('name', 'email', 'created_at')

admin.site.register(Order, OrderAdmin)


# admin.site.register(Order)