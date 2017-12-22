from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from .views import VideoArchiveIndexView, VideoDateDetailView, VideoDateView, VideoDayArchiveView, VideoDetailView, VideoListView, VideoMonthArchiveView, VideoYearArchiveView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('videocapture:video-archive'), permanent=True),
        name='root'),
    url(r'^video/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
        VideoDateDetailView.as_view(month_format='%m'),
        name='video-detail'),
    url(r'^video/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
        VideoDayArchiveView.as_view(month_format='%m'),
        name='video-archive-day'),
    url(r'^video/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
        VideoMonthArchiveView.as_view(month_format='%m'),
        name='video-archive-month'),
    url(r'^video/(?P<year>\d{4})/$',
        VideoYearArchiveView.as_view(),
        name='video-archive-year'),
    url(r'^video/$',
        VideoArchiveIndexView.as_view(),
        name='video-archive'),

    url(r'^video/(?P<slug>[\-\d\w]+)/$',
        VideoDetailView.as_view(),
        name='watch-video'),
    url(r'^videolist/$',
        VideoListView.as_view(),
        name='video-list'),
]