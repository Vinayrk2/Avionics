from django import forms
from django.forms import JSONField, Textarea
from .models import Service, AboutSection

class ServiceForm(forms.ModelForm):
    specifications = JSONField(widget=forms.Textarea(attrs={'rows': 4,'id':'features'}), required=False)
    technical_information = JSONField(widget=forms.Textarea(attrs={'rows': 4,'id':'technical_info'}), required=False)
     
    class Meta:
        model = Service
        fields = '__all__'

class AboutSectionForm(forms.ModelForm):
    column = JSONField(widget=forms.Textarea(attrs={'rows': 4,'id':'about_column'}), required=False)
    
    class Meta:
        model = AboutSection
        fields = ['title', 'description', 'column']
        