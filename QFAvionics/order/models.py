from django.db import models
from django.utils.timezone import now   
from user.models import CustomUser

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    status = models.CharField(max_length=50, blank=False, null=False, default='pending')
    invoice_id = models.CharField(max_length=100,  blank=False, null=False)
    state = models.CharField(max_length=20, blank=False, null=False, default='Ordered')
    order_id = models.CharField(max_length=30,  blank=False, null=False)
    create_time = models.DateField(auto_created=True)
    payer_email = models.CharField(max_length=100, blank=False, null=False)
    payer_id = models.CharField(max_length=100, blank=False, null=False)
    items = models.JSONField(default=dict)
    address = models.TextField(max_length=300, blank=False)
    
    def __str__(self):
        return self.order_id