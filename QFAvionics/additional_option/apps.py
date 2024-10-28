from django.apps import AppConfig

class AdditionalOptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'additional_option'

    def ready(self):
        from django.conf import settings
        from .utils import get_setting
        # Dynamically load settings values from the database
        # settings.SITE_NAME = get_setting("site_name")
        # settings.ENABLE_FEATURE = get_setting("enable_feature")
        print(get_setting("currency_rate"))
        settings.CURRENCY_EXCHANGE_RATE = get_setting("currency_rate")