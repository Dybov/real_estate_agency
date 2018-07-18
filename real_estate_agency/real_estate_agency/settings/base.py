"""
Django settings for real_estate_agency project.
Generated by 'django-admin startproject' using Django 1.10.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECRET_KEY must set in the child settings file
# DEBUG must set in the child settings file
# ALLOWED_HOSTS must set in the child settings file

# Application definition
# dal is django-autocomplete-light
# https://github.com/yourlabs/django-autocomplete-light
INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'address',
    'real_estate',
    'new_buildings',
    'mortgage',
    'contacts',
    'feedback',
    'company',
    'applications',
    'resale',
    'imagekit',
    'phonenumber_field',
    'celery',
    'django_unused_media',
    'django_bootstrap_breadcrumbs',
    'analytical',
    'adminsortable2',
    'django_celery_beat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'applications.middleware.UTMMiddleware',
]

ROOT_URLCONF = 'real_estate_agency.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'contacts.views.default_contacts_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'real_estate_agency.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
# Must set in the child settings file

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation\
            .UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation\
            .MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation\
            .CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation\
            .NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ' '

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Set Telegram for production
TELEGRAM_TOKEN = ''
TELEGRAM_CHATS = []
TELEGRAM_ADMINS_CHATS = []

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Don't forget to set your token to production
VIBER_BOT_TOKEN = 'your-secret-token'
VIBER_BOT_NAME = 'domus72.ru'
VIBER_BOT_AVATAR = 'http://viber.com/avatar.jpg'
VIBER_BOT_PRIVATE_GROUPS = []

# Use viber ids
VIBER_BOT_TEST_ADMINS = []
