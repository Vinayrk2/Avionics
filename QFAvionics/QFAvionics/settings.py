"""
Django settings for QFAvionics project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kj)^s7oyb9j$6x@kactjg7ar$-7_&jys@&+v5jber@+=$*9db%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',"localhost"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'product',
    'user',
    'cart',
    'shopcart',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'QFAvionics.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'QFAvionics.header_context.header_options',
                'cart.context_processor.cart_total_amount'
            ],
        },
    },
]

WSGI_APPLICATION = 'QFAvionics.wsgi.application'

CART_SESSION_ID = 'cart'   
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Where to look for static files in development
]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # Collect static files for deployment
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/' 
# Directory to collect static files (for production)
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),  # Where to look for static files in development
# ]

# # Collect static files for deployment
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  #

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.CustomUser'  # Adjust the app name if necessary


""" REquired for manager for tax and shipping and additional charges"""

CHARGES = {
    "tax":0.01,
    "shipping": 10.0,
    "additional": 5.0
}

"""session related"""

SESSION_COOKIE_AGE = 18000  # Session expires in 30 minutes
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Don't expire on browser close
# SESSION_SAVE_EVERY_REQUEST = True  # Reset session expiration time on every request
# SESSION_COOKIE_SECURE = True  # Use this if you're using HTTPS