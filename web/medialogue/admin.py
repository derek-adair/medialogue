from django.contrib import admin
from .models import MediaGallery as Album, Video

from video_encoding.admin import FormatInline

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
   inlines = (FormatInline,)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass
