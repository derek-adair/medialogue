from django.contrib import admin
from .models import Album, Video, Photo

from video_encoding.admin import FormatInline

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
   inlines = (FormatInline,)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
   inlines = (FormatInline,)
