"""
Django settings for real_estate_agency project.
"""

try:
    from .production import *
except Exception as e:
    from .develop import *

if not TELEGRAM_TOKEN:
    raise Exception("Telegram token is required")