from django.db import models
from django.utils.timezone import now   
from user.models import CustomUser

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipping','Shipping'),
        ('outfordelivery', 'Out For Delivery'),
        ('completed', 'Order Completed'),
    ]
        
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', null=False)
    order_date = models.DateTimeField(auto_now_add=True, editable=False)
    amount_summary = models.JSONField(default=dict, blank=False,  null=False)
    payment_status = models.CharField(max_length=50, blank=False, null=False, default='pending')
    order_id = models.CharField(max_length=30,  blank=False, null=False)
    payer_id = models.CharField(max_length=100, blank=False, null=False)
    items = models.JSONField(default=dict, null=False,  blank=False)
    address = models.JSONField(default=dict, null=False, blank=False)
    state = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=40, blank=False, null=False)

    # Add the 'status' field using choices
    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'order_date': self.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'amount_summary': self.amount_summary,
            'status': self.payment_status,
            'order_id': self.order_id,
            'payer_id': self.payer_id,
            'products': self.items,
            'address': self.address,
            'state': self.state,
            'transaction_id': self.transaction_id
        }
    
    def __str__(self):
        return self.order_id