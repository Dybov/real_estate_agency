from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^obratnyj-zvonok/$', views.Callback.as_view(), name='callback'),
]
