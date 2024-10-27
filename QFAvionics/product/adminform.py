from django import forms
from django.forms import JSONField
from .models import Product

class ProductForm(forms.ModelForm):
    features = JSONField(widget=forms.Textarea(attrs={'rows': 4,'id':'features1'}), required=False)

    class Meta:
        model = Product
        fields = '__all__'
