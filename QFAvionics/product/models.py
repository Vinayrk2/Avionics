from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)  
    category = models.OneToOneField('Category', blank=True, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)  # New field for active status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    images = models.ManyToManyField('Image', blank=True)

    def __str__(self):
        return self.name

    def get_images(self):
        """Retrieve all images associated with the product."""
        return self.images.all()

    def update_details(self, name=None, description=None, price=None, weight=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if price is not None:
            self.price = price
        if weight is not None:
            self.weight = weight
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


class Image(models.Model):
    image = models.ImageField(upload_to="static/product/images/")


class Category(models.Model):
    name = models.TextField(blank=False, default="", max_length=100)
    image = models.ImageField(upload_to="static/product/category/", blank=True)
    
    def __str__(self):
        return self.name