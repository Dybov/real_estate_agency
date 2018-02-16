from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^callback/$', views.Callback.as_view(), name='callback'),
]
