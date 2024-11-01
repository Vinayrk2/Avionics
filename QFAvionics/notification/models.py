from django.db import models

# notification_type_choices = [
#     ('new_comment', 'New Comment'),
#     ('new_product', 'New Product'),
#     ('contact_update', 'Contact Update'),
#     ('policy_update', 'Policies Updated'),
#     ('new_product_review', 'New Product Review'),
#     ('new_product_rating', 'New Product Rating'),
#     ('new_product_comment', 'New Product Comment'),
#     ('notify_user', 'Update For Users'),
#     ('offer_update','New Offer'),
#     ('news','News'),
# ]
class News(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=False, null=False)
    image = models.ImageField(upload_to="static/notification/images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.URLField(blank=True, null=True, default="")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
