from django import forms
from django.forms import JSONField
from .models import Service

class ServiceForm(forms.ModelForm):
    specifications = JSONField(widget=forms.Textarea(attrs={'rows': 4,'id':'features'}), required=False)
    technical_information = JSONField(widget=forms.Textarea(attrs={'rows': 4,'id':'technical_info'}), required=False)
     
    class Meta:
        model = Service
        fields = '__all__'
