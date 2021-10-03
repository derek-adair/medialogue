from django.contrib import admin
from .models import MediaGallery, Video

from video_encoding.admin import FormatInline

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
   inlines = (FormatInline,)

@admin.register(MediaGallery)
class MediaGalleryAdmin(admin.ModelAdmin):
    pass
