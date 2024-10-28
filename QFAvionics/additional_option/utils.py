# In yourapp/settings_manager.py
from django.core.cache import cache
from .models import SiteSettings

def get_setting(name):
    # Try to retrieve settings from the cache
    settings = cache.get('site_settings', False)
    
    if not settings:
        
        settings = SiteSettings.load()
        
        cache.set('site_settings', settings, timeout=300)  

    # Retrieve the requested setting attribute
    return getattr(settings, name, None)
