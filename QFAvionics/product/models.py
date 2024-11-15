from django.db import models
from django.conf import settings


CURRENCY_CHOICES = [
    ('USD', 'USD'),
    ('CAD', 'CAD'),
]

class Product(models.Model):
    name = models.CharField(max_length=255)
    part_number = models.CharField(blank=True, null=True, default=None, unique=True, max_length=30)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    features = models.JSONField(default=dict)
    more_details = models.URLField(default="", null=True, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True, default="")
    condition = models.CharField(max_length=50, blank=True, null=True, default="")
    availability = models.CharField(max_length=50, blank=True, null=True, default="")
    
    @property
    def image(self):
        # Return the URL of the first image associated with this product
        first_image = self.images.first()  # Access related images
        return first_image.image if first_image else DefaultImage()
    
    def get_related_products(self,request):
        product_temp = Product.objects.filter(category=self.category).exclude(id=self.id)[:8]
        products = []
        for product in product_temp:
            products.append(product.to_dict(request))
        return products
    
    def __str__(self):
        return self.name

    def get_image(self):
        """Retrieve all images associated with the product."""
        if  self.images.exists():
            return self.images.all()[0].image
        else:
            image = DefaultImage()
            # image.url = "https://img-s-msn-com.akamaized.net/tenant/amp/entityid/AA1sDmEk.img?w=612&h=304&q=90&m=6&f=webp&x=587&y=269&u=t" 
            return image
    def update_details(self, name=None, description=None, price=None, weight=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if price is not None:
            self.price = price
        self.save()

    def apply_discount(self, percentage):
        if 0 <= percentage <= 100:
            discount_amount = (percentage / 100) * self.price
            self.price -= discount_amount
            self.save()
        else:
            raise ValueError("Discount percentage must be between 0 and 100.")

    def to_dict(self,request):
        obj = {
            'name': self.name,
            'description': self.description,
            # 'price': str(self.price),  # Convert to string for JSON serialization
            'part_number': self.part_number,
            'category': self.category if self.category else None,  # Use category ID or None
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'id':self.pk,
            'image': self.get_image(),
            'features': self.features,
            'condition': self.condition,
            'availability': self.availability,
            'manufacturer': self.manufacturer,
            'more_details': self.more_details,
            # 'images': [image.id for image in self.images.all()]  # List of image IDs
        }
        
        if request.user.is_authenticated:
            if request.session.get("currency"):
                if  request.session.get("currency") == "USD":
                    obj['price'] = round(float(self.price) * float(settings.CURRENCY_EXCHANGE_RATE),2)
                    obj['currency'] = "USD"
                else:
                    obj['price'] = round(float(self.price),2)
                    obj['currency'] = "CAD"
            else:
                obj['price'] = round(float(self.price),2)
                obj['currency'] = "CAD"
        else:
            obj['price'] = ''
        return obj
        

class DefaultImage():
    url = "/static/images/defult.png"
    
        

class Image(models.Model):
    image = models.ImageField(upload_to="static/product/images/")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images', blank=True) 


class Category(models.Model):
    name = models.TextField(blank=False, default="", max_length=100)
    image = models.ImageField(upload_to="static/product/category/", blank=True, default="defult.png")
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name