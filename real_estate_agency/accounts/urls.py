from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^change-profile/$', views.change_own_profile, name='change-profile'),
]
