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

from .views import (about,
                    mortgage,
                    feedback,
                    corporation_benefit_plan,
                    contacts,
                    )


urlpatterns = [
    url(r'^', include('new_buildings.urls'), name='new_buildings'),
    url(r'^address/', include('address.urls'), name='address'),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^about/', about, name='about'),
    url(r'^mortgage/', include('mortgage.urls', namespace='mortgage')),
    url(r'^feedback/', feedback, name='feedback'),
    url(r'^corporation_benefit_plan/', corporation_benefit_plan, name='corporation_benefit_plan'),
    url(r'^contacts/', contacts, name='contacts'),
]

#For using this path at dev machines
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 