from django.conf.urls import url

from .views import ResaleListView, detailed


urlpatterns = [
    url(r'^$', ResaleListView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', detailed, name='detailed'),
]
