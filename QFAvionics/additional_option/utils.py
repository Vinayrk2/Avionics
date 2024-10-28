# In yourapp/settings_manager.py
from django.core.cache import cache
from .models import SiteSettings

def get_setting(name):
    # Try to retrieve settings from the cache
    settings = cache.get('site_settings', False)
    
    if not settings:
        # If cache is empty, load settings from the database
        settings = SiteSettings.load()
        # Cache the settings with a timeout (e.g., 300 seconds)
        cache.set('site_settings', settings, timeout=300)  # Cache for 5 minutes

    # Retrieve the requested setting attribute
    return getattr(settings, name, None)
