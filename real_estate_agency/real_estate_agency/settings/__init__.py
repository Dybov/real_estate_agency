"""
Django settings for real_estate_agency project.
"""

try:
    from .production import *
except Exception as e:
    from .develop import *
