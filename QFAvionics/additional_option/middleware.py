from django.conf import settings
from .utils import get_setting

def setting_middleware(get_response):
    # One-time setup to set the currency rate in settings
    def set_currency_rate():
        setting = get_setting()
        settings.CURRENCY_EXCHANGE_RATE = setting.currency_rate
        # settings.DEFAULT_FROM_EMAIL = setting.bussiness_email
        # settings.EMAIL_HOST_USER = setting.bussiness_email
        # settings.EMAIL_HOST_PASSWORD = setting.email_app_password
        settings.CHARGES["tax"] = setting.tax

    set_currency_rate()
    
    return {}
