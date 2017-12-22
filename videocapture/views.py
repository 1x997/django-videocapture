# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.dates import ArchiveIndexView, DateDetailView, DayArchiveView, MonthArchiveView, \
    YearArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Video

# Create your views here.

class VideoListView(ListView):
    queryset = Video.objects.all()
    paginate_by = 20


class VideoDetailView(DetailView):
    queryset = Video.objects.all()
    template_name = 'videocapture/watch_video.html'


class VideoDateView(object):
    queryset = Video.objects.all()
    date_field = 'dateFilmed'
    allow_empty = True


class VideoDateDetailView(VideoDateView, DateDetailView):
    pass


class VideoArchiveIndexView(VideoDateView, ArchiveIndexView):
    template_name = 'videocapture/videos.html'


class VideoDayArchiveView(VideoDateView, DayArchiveView):
    pass


class VideoMonthArchiveView(VideoDateView, MonthArchiveView):
    pass


class VideoYearArchiveView(VideoDateView, YearArchiveView):
    make_object_list = True