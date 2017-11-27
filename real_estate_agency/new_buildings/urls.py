from django.conf.urls import url

from . import views
from .apps import NewBuildingsConfig

app_name = NewBuildingsConfig.name

urlpatterns = [
    url(r'^$', views.ResidentalComplexList.as_view(),
        name='residental-complex-list'),
    url(r'^new-buildings/(?P<pk>\d+)/$',
        views.ResidentalComplexDetail.as_view(),
        name='residental-complex-detail',
        ),
]
