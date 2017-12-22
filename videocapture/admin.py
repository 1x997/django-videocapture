# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Video

# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['video', 'dateFilmed']
        else:
            return []
    
    class Meta:
        model = Video
admin.site.register(Video, VideoAdmin)