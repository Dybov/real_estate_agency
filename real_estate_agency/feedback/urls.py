from django.conf.urls import url

from .views import FeedbackList


urlpatterns = [
    url(r'^$', FeedbackList.as_view(), name='index'),
]