# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import cv2
from PIL import Image

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from .validators import validate_file_extension

def video_upload_location(instance, filename):
    return 'videocapture/videos/' + str(instance.dateFilmed.year) + '/' + str(instance.dateFilmed.month) + '/' + filename

# Create your models here.
class Video(models.Model):
    video = models.FileField(upload_to=video_upload_location, validators=[validate_file_extension], help_text='The video to uploading to the site. Not editable after upload.')
    title = models.CharField(unique=True, max_length=50, null=False, blank=False, help_text='Title for the video. This is editable after upload.')
    slug = models.SlugField(unique=True, editable=False, null=False, blank=True, default='')
    dateFilmed = models.DateField(null=False, blank=False, help_text='The date when this video was filmed. Not editable after upload.')
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        is_new = self.pk
        old_slug = self.slug
        try:
            Video.objects.get(title=self.title)
            is_new_title = False
        except Video.DoesNotExist:
            is_new_title = True
        if is_new_title:
            self.slug = slugify(self.title)
            try:
                while(True):
                    Video.objects.get(slug=self.slug)
                    self.slug += '0'
            except Video.DoesNotExist:
                pass
        super(Video, self).save(*args, **kwargs)
        if is_new is None:
            videocap = cv2.VideoCapture(self.video.path)
            success, thumbnail = videocap.read()
            path = os.path.join(settings.MEDIA_ROOT, "videocapture", "thumbnails", (self.slug + '.thumbnail.jpg'))
            cv2.imwrite(path, thumbnail)
            im = Image.open(path)
            size = (300, 150)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(path, "JPEG")
        else:
            os.rename(os.path.join(settings.MEDIA_ROOT, "videocapture", "thumbnails", (old_slug + '.thumbnail.jpg')), os.path.join(settings.MEDIA_ROOT, "videocapture", "thumbnails", (self.slug + '.thumbnail.jpg')))
            
    def delete(self, *args, **kwargs):
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, "videocapture", "thumbnails", (self.slug + '.thumbnail.jpg'))
        video_path = self.video.path
        os.remove(thumbnail_path)
        os.remove(video_path)
        
        super(Video, self).delete(*args, **kwargs)
    
    def get_thumbnail_url(self):
        return os.path.join(settings.MEDIA_URL, "videocapture", "thumbnails", (self.slug + '.thumbnail.jpg'))
    
    def get_video_url(self):
        return os.path.join(settings.MEDIA_URL, self.video.name)
    
    def get_watch_video_url(self):
        return reverse('videocapture:watch-video', args=[self.slug])
    
    def get_video_type(self):
        if os.path.splitext(self.video.name)[1] == '.mp4':
            return 'video/mp4'
        else:
            return 'video/ogg'
        
    