from django.db import models

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=40, default='', blank=False, null=False)
    image = models.ImageField(upload_to='static/service/images/')
    status = models.BooleanField(default=True)
    description = models.TextField(default='')
    service_type = models.CharField(default='', max_length=40, blank=False, null=False)

    def __str__(self):
        return self.name
    
class Link(models.Model):
    name = models.CharField(max_length=40, default='', blank=False, null=False)
    url = models.CharField(max_length=100, default='', blank=False, null=False)
    
    def __str__(self):
        return self.name
    
from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=70, blank=False, null=False)
    phone_number_1 = models.IntegerField(blank=True, null=True)
    phone_number_2 = models.IntegerField(blank=True, null=True)
    bussiness_email = models.EmailField(max_length=70, blank=False, null=False, help_text="Email on which receive the email")
    product_default_price_show = models.BooleanField(default=True)

    def __str__(self):
        return self.site_name

    