from django.db import models
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_migrate
from django.core.exceptions import ValidationError

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=40, default='', blank=False, null=False)
    image = models.ImageField(upload_to='static/service/images/', default="defult.png")
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
    
    class Meta:
        verbose_name = 'Important Link'
        verbose_name_plural = 'Important Links'
    

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="QFAvionics")
    email = models.EmailField(max_length=70, blank=False, null=False,  default='info@qfavionics.com')
    phone_number_1 = models.CharField(blank=True, null=True, max_length=10)
    phone_number_2 = models.CharField(blank=True, null=True, max_length=10)
    bussiness_email = models.EmailField(max_length=70, blank=False, default='info@qfavionics.com', null=False, help_text="Email on which receive the email")
    currency_rate = models.DecimalField(null=False, blank=False, default=0.72, decimal_places=2, max_digits=3)
    address = models.TextField(default="QF Avionics Center LtdHangar #11 Airport Drive, Springbook,ABT4S 2E8Canada", blank=True, null=True)
    airport = models.TextField(default="Red Deer Regional Airport, CYQF, YQF", blank=True, null=True)
    email_app_password = models.TextField(max_length=30,  default="zochakahgfehnxdq", blank=True, null=True)
    tax = models.DecimalField(decimal_places=2,  max_digits=5, default=0.15, null=False, blank=False)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def get_footer_data(self):
        return {
            "location": self.address,
            "airport": self.airport,
            "instagram": self.instagram,
            "youtube": self.youtube,
            "linkedin": self.linkedin
        }
    
    def get_header_data(self):
        return {
            "site_name": self.site_name,
            "email": self.email,
            "phone_number": self.phone_number_1,
        }
    
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
        
    @classmethod
    def get_instance(cls):
        instance, created = cls.objects.get_or_create(id=1)
        return instance
    
    @receiver(post_migrate)
    def create_singleton_instance(sender, **kwargs):
        if sender.name == "additional_option":
            SiteSettings.get_instance()
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
    
    
class AboutContent(models.Model):
    class Meta:
        verbose_name = "About Content"
        verbose_name_plural = "About Description"
        
    main_description = models.TextField(default='Serving all of Western Canada, we offer sales of new and used equipment as well as installations on both commercial and private planes. We specialize in avionics line maintenance, retrofits and component repairs. We’re a Transport Canada approved organization and have been in business since 1979, serving all sectors of the aviation industry.', blank=False, null=False)
    field1 = models.CharField(max_length=20, default='Mission', blank=False, help_text='first card name')
    field1_Description = models.TextField(max_length=800, default='To be an enduring company by creating superior products for automotive, aviation, marine, outdoor, and sports that are an essential part of our customers lives.', help_text='Enter description for field1')
    field2 = models.CharField(max_length=20, default='Vision', blank=False, help_text='second card name')
    field2_Description = models.TextField(max_length=800, default='The Aviation Gateway and Key Economic Driver for Central Alberta', help_text='Enter description for field2')
    field3 = models.CharField(max_length=20, default='VALUES', blank=False, help_text='third card name')
    field3_Description = models.TextField(max_length=800, default='The foundation of our culture is honesty, integrity, and respect for associates, customers, and business partners. Each associate is fully committed to serving customers and fellow associates through outstanding performance and accomplishing what we say we will do.', help_text='Enter description for field3')

    def save(self, *args, **kwargs):
        self.pk = 1        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return "About Us Page"
    
    @classmethod
    def get_instance(cls):
        instance, created = cls.objects.get_or_create(id=1)
        return instance
    
    @receiver(post_migrate)
    def create_singleton_instance(sender, **kwargs):
        if sender.name == "additional_option":
            AboutContent.get_instance()

class AboutSection(models.Model):
    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Page Sections"
    
    about = models.ForeignKey('AboutContent', on_delete=models.CASCADE, related_name='sections', blank=True, null=True) 
    title = models.CharField(max_length=50, blank=False, default='', null=False)
    description = models.TextField(max_length=100, blank=True, default='', help_text='it is optional to have the description')
    column = models.JSONField(default=dict)
    
    def save(self, *args, **kwargs):
        self.about = AboutContent.objects.filter(pk=1).first()        
        super().save(*args, **kwargs)

    def  __str__(self):
        return self.title

        
class HomeSection(models.Model):
    class Meta:
        verbose_name = "What We Do"
        verbose_name_plural = "What We Do"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "Home Section"
    
    @classmethod
    def get_instance(cls):
        instance, created = cls.objects.get_or_create(id=1)
        return instance
    
    @receiver(post_migrate)
    def create_singleton_instance(sender, **kwargs):
        if sender.name == "additional_option":
            HomeSection.get_instance()

class HomeSectionItem(models.Model):
    home = models.ForeignKey(HomeSection, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=210, blank=False, null=False)
    image = models.ImageField(blank=True, upload_to='static/images/whatwedo', default="defult.png")

    class Meta:
        verbose_name = "Home Section Item"
        verbose_name_plural = "Home Section Items"

    def save(self, *args, **kwargs):
        # Limit the number of items to 6
        if self.home.items.count() >= 6 and not self.pk:
            raise ValidationError("You can only add up to 6 items for the Home Section.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class CarasoleImage(models.Model):
    image = models.ImageField(upload_to='static/images/carousel', default="defult.png")
    home = models.ForeignKey(HomeSection, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = "Home Slider Images"
        verbose_name_plural = "Home Slider Images"

    def __str__(self):
        return "Image - {}".format(self.pk)
    
class GalaryItem(models.Model):
    heading = models.CharField(max_length=250, default="")
    
    def __str__(self):
        return self.heading
    
    @property
    def image(self):
        # Return the URL of the first image associated with this product
        first_image = self.subitems.first()  # Access related images
        return first_image.image if first_image else DefaultImage()    
    
    # @property
    # def subitems(self):
    #     # Return the sub details for the galary item
    #     return self.images.all()  # Access related subitems
    class Meta:
        verbose_name = "Galary"
        verbose_name_plural = "Galary"
    
class DefaultImage():
    url = "/static/images/defult.png"
    
class GalaryItemDetail(models.Model):
    galaryItem = models.ForeignKey('GalaryItem', related_name='subitems', on_delete=models.CASCADE, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='static/images/galary', blank=True, null=True, help_text="Upload image for the gallery item")
    
    def __str__(self):
        return self.description