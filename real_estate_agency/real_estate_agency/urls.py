"""real_estate_agency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from .views import (corporation_benefit_plan,
                    index,
                    privacy_policy,
                    thanks
                    )


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^new-buildings/', include('new_buildings.urls', namespace='new_buildings')),
    url(r'^address/', include('address.urls', namespace='address')),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^about/', include('company.urls', namespace='company')),
    url(r'^ipoteka/', include('mortgage.urls', namespace='mortgage')),
    url(r'^feedback/', include('feedback.urls', namespace='feedback')),
    url(r'^corporation_benefit_plan/', corporation_benefit_plan, name='corporation_benefit_plan'),
    url(r'^contacts/', include('contacts.urls', namespace='contacts')),
    url(r'^applications/', include('applications.urls', namespace='applications')),
    url(r'^privacy-policy/', privacy_policy, name='privacy-policy'), 
    url(r'^thanks/', thanks, name='thanks'), 
]

#For using this path at dev machines
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 
    try:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass