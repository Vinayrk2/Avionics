from django.db import models

notification_type_choices = [
    ('new_comment', 'New Comment'),
    ('new_product', 'New Product'),
    ('contact_update', 'Contact Update'),
    ('policy_update', 'Policies Updated'),
    ('new_product_review', 'New Product Review'),
    ('new_product_rating', 'New Product Rating'),
    ('new_product_comment', 'New Product Comment'),
    ('notify_user', 'Update For Users'),
    ('offer_update','New Offer'),
    ('news','News'),
]
class Notification(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=False, null=False)
    image = models.ImageField(upload_to="static/notification/images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notification_type = models.CharField(max_length=50,  blank=False, null=False, choices=notification_type_choices,  default='news')
    additional_write = models.TextField(default='', blank=True, null=True,  max_length=1000)

    def __str__(self):
        return self.title
