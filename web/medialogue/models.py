from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from video_encoding.fields import VideoField
from video_encoding.models import Format
# imports
from sortedm2m.fields import SortedManyToManyField
from photologue.models import Gallery

class Video(models.Model):
    width = models.PositiveIntegerField(editable=False, null=True)
    height = models.PositiveIntegerField(editable=False, null=True)
    duration = models.FloatField(editable=False, null=True)
    file = VideoField(
        width_field='width',
	height_field='height',
	duration_field='duration'
	)
    format_set = GenericRelation(Format)

    def __str__(self):
        return self.file.name

class MediaGallery(Gallery):
    videos = SortedManyToManyField(
        'medialogue.Video',
	related_name='galleries',
	verbose_name=('videos'),
	blank=True
    )
