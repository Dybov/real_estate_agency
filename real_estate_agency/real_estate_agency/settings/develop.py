"""
Django settings for real_estate_agency project development.
"""

from .base import *


# Dev key
SECRET_KEY = 'HrenTebem2^0vp4uc7tj+yu+lw+on=^z8br4t_aefjk$32@m_12^gof271'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# INSTALLED_APPS += ['debug_toolbar']