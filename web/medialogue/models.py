from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.utils.timezone import now
from django.urls import reverse

from video_encoding.fields import VideoField
from video_encoding.models import Format

from sortedm2m.fields import SortedManyToManyField
from photologue.models import Gallery, add_default_site
from photologue.managers import SharedQueries

class SharedQueries(models.query.QuerySet):
    def on_site(self):
        """Return objects linked to the current site only."""
        return self.filter(sites__id=settings.SITE_ID)
    def is_public(self):
        return self.filter(is_public=True)

class Video(models.Model):
    """
    Video version of photologue.models.Photo
    NOTE -  Calls post_save connected in apps.py/signals.py
                 - medialogue.tasks.create_thumbnail 
                 - django_video_encoding.tasks.convert_all_videos
    """
    objects = SharedQueries.as_manager()
    # Meta Fields
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True,
                            max_length=250,
                            help_text='A "slug" is a unique URL-friendly title for an object.')
    caption = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=now)
    thumbnail = models.ImageField(blank=True)
    sites = models.ManyToManyField(Site, verbose_name='sites', blank=True)
    format_set = GenericRelation(Format)
    # video detail fields
    width = models.PositiveIntegerField(editable=False, null=True)
    height = models.PositiveIntegerField(editable=False, null=True)
    duration = models.FloatField(editable=False, null=True)
    file = VideoField(
        width_field='width',
	height_field='height',
	duration_field='duration'
	)

    def get_absolute_url(self):
        return reverse("medialogue:ml-video", args=[self.slug])

    def __str__(self):
        return self.title

# Auto add the current site
models.signals.post_save.connect(add_default_site, sender=Video)

class MediaGallery(Gallery):
    videos = SortedManyToManyField(
        'medialogue.Video',
	related_name='galleries',
	verbose_name=('videos'),
	blank=True
    )

    def get_absolute_url(self):
        return reverse('medialogue:ml-gallery', args=[self.slug])
