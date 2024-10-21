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