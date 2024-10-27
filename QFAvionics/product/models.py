from django.db import models
from django.conf import settings


CURRENCY_CHOICES = [
    ('USD', 'USD'),
    ('CAD', 'CAD'),
]

class Product(models.Model):
    name = models.CharField(max_length=255)
    part_number = models.DecimalField(blank=True, null=True, unique=True, max_digits=20, decimal_places=0)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # currency = models.CharField(max_length=3,  choices=CURRENCY_CHOICES, default='CAD')
    stock_quantity = models.PositiveIntegerField(default=0)  
    category = models.ForeignKey('Category', blank=True, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    features = models.JSONField()
    
    def get_related_products(self,request):
        product_temp = Product.objects.filter(category=self.category).exclude(id=self.id)[:10]
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

    def is_in_stock(self):
        if self.stock_quantity >= 0:
            return False
        # Implement stock logic here
        return True  # Placeholder return value
    
    def to_dict(self,request):
        obj = {
            'name': self.name,
            'description': self.description,
            # 'price': str(self.price),  # Convert to string for JSON serialization
            'stock_quantity': self.stock_quantity,
            'category': self.category if self.category else None,  # Use category ID or None
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'id':self.pk,
            'image': self.get_image(),
            'features': self.features
            # 'images': [image.id for image in self.images.all()]  # List of image IDs
        }
        
        if request.user.is_authenticated:
            if request.session.get("currency"):
                if  request.session.get("currency") == "USD":
                    obj['price'] = round(float(self.price) * settings.CURRENCY_EXCHANGE_RATE,2)
                    obj['currency'] = "USD"
                else:
                    obj['price'] = round(float(self.price),2)
                    obj['currency'] = "CAD"
            else:
                obj['price'] = round(float(self.price),2)
                obj['currency'] = "CAD"
        else:
            obj['price'] = 'login to view the price'
        return obj
        

class DefaultImage():
    url = "/static/images/defult.png"
    
        

class Image(models.Model):
    image = models.ImageField(upload_to="static/product/images/")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images', blank=True)  # Link image to product


class Category(models.Model):
    name = models.TextField(blank=False, default="", max_length=100)
    image = models.ImageField(upload_to="static/product/category/", blank=True)
    
    def __str__(self):
        return self.name