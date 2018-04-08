from django.conf.urls import url
from . import views


app_name = 'real_estate'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^privacy-policy$', views.privacy_policy, name='privacy-policy'),
]
