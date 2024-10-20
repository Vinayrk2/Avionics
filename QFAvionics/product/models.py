from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)  
    category = models.ForeignKey('Category', blank=True, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)  # New field for active status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def get_image(self):
        """Retrieve all images associated with the product."""
        return self.images.all()[0].image

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
    
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': str(self.price),  # Convert to string for JSON serialization
            'weight': str(self.weight),  # Convert to string for JSON serialization
            'stock_quantity': self.stock_quantity,
            'category': self.category if self.category else None,  # Use category ID or None
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            # 'images': [image.id for image in self.images.all()]  # List of image IDs
        }


class Image(models.Model):
    image = models.ImageField(upload_to="static/product/images/")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images', blank=True)  # Link image to product


class Category(models.Model):
    name = models.TextField(blank=False, default="", max_length=100)
    image = models.ImageField(upload_to="static/product/category/", blank=True)
    
    def __str__(self):
        return self.name