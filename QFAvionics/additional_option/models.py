from django.db import models
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=40, default='', blank=False, null=False)
    image = models.ImageField(upload_to='static/service/images/')
    status = models.BooleanField(default=True)
    description = models.TextField(default='')
    service_type = models.CharField(default='', max_length=40, blank=False, null=False)
    specifications = models.JSONField(default=dict)
    technical_information = models.JSONField(default=dict)

    def __str__(self):
        return self.name
    
class Link(models.Model):
    name = models.CharField(max_length=40, default='', blank=False, null=False)
    url = models.CharField(max_length=100, default='', blank=False, null=False)
    
    def __str__(self):
        return self.name
    

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="QFAvionics")
    email = models.EmailField(max_length=70, blank=False, null=False,  default='info@qfavionics.com')
    phone_number_1 = models.IntegerField(blank=True, null=True, default='14038864326')
    phone_number_2 = models.IntegerField(blank=True, null=True)
    bussiness_email = models.EmailField(max_length=70, blank=False, default='info@qfavionics.com', null=False, help_text="Email on which receive the email")
    currency_rate = models.DecimalField(null=False, blank=False, default=0.72, decimal_places=2, max_digits=3)
    address = models.TextField(default="QF Avionics Center LtdHangar #11 Airport Drive, Springbook,ABT4S 2E8Canada", blank=True, null=True)
    airport = models.TextField(default="Red Deer Regional Airport, CYQF, YQF", blank=True, null=True)
    email_app_password = models.TextField(max_length=30,  default="zochakahgfehnxdq", blank=True, null=True)
    tax = models.DecimalField(decimal_places=2,  max_digits=5, default=0.15, null=False, blank=False)


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
        self.pk = 1        
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        # Create a default instance if none exists
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
@receiver(post_save, sender=SiteSettings)
def clear_site_settings_cache(sender, **kwargs):
    print("Clearing site settings")
    cache.delete('site_settings')