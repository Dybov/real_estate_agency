from django.conf.urls import url
from . import views


app_name = 'real_etate'

urlpatterns = [
    url(r'^$', views.index),
]
