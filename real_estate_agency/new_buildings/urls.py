from django.conf.urls import url

from . import views
from .apps import NewBuildingsConfig

app_name = NewBuildingsConfig.name

urlpatterns = [
    url(r'^$', views.ResidentalComplexList.as_view(),
        name='residental-complex-list'),
    url(r'^(?P<pk>\d+)/$',
        views.ResidentalComplexDetail.as_view(),
        name='residental-complex-detail',
        ),
    url(r'^feeds/yandex-new-buildings$',
        views.NewApartmentsFeed.as_view(),
        name='new-aparments-feed',
        ),
]
