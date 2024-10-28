from django.db import models
from django.core.cache import cache

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
    

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=70, blank=False, null=False)
    phone_number_1 = models.IntegerField(blank=True, null=True)
    phone_number_2 = models.IntegerField(blank=True, null=True)
    bussiness_email = models.EmailField(max_length=70, blank=False, null=False, help_text="Email on which receive the email")
    currency_rate = models.IntegerField(null=False, blank=False, default=0.72)
    address = models.TextField(default="QF Avionics Center LtdHangar #11 Airport Drive, Springbook,ABT4S 2E8Canada", blank=True, null=True)
    airport = models.TextField(default="Red Deer Regional Airport, CYQF, YQF", blank=True, null=True)

    def __str__(self):
        return "Website Settings"

    def to_dict(self):
        return {
            "site_name": self.site_name,
            "email": self.email,
            "phone_number_1": self.phone_number_1,
            "phone_number_2": self.phone_number_2,
            "bussiness_email": self.bussiness_email,
            "currency_rate": self.currency_rate,
            "address": self.address,
            "airport": self.airport
        }
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
        
    def save(self, *args, **kwargs):
        # Ensure only one instance exists by setting a fixed primary key
        self.pk = 1

        # Clear the cached settings before saving the new settings
        cache.delete('site_settings')

        # Call the original save method to save the instance
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        # Create a default instance if none exists
        obj, created = cls.objects.get_or_create(pk=1)
        return obj