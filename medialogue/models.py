import os
import unicodedata
from PIL import Image
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import filepath_to_uri, force_str, smart_str
from django.db import models
from django.db.models.signals import post_save
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.utils.timezone import now
from django.urls import reverse

from .utils import _generate_slug
from video_encoding.fields import VideoField
from video_encoding.models import Format

from ordered_model.models import OrderedModel, OrderedModelManager, OrderedModelQuerySet

import logging
logger = logging.getLogger(__name__)

# Default limit for album.latest
LATEST_LIMIT = getattr(settings, 'MEDIALOGUE_GALLERY_LATEST_LIMIT', None)

# Number of random images from the album to display.
SAMPLE_SIZE = getattr(settings, 'MEDIALOGUE_GALLERY_SAMPLE_SIZE', 5)

# max_length setting for the ImageModel ImageField
IMAGE_FIELD_MAX_LENGTH = getattr(settings, 'MEDIALOGUE_IMAGE_FIELD_MAX_LENGTH', 100)

# Medialogue image path relative to media root
MEDIALOGUE_DIR = getattr(settings, 'MEDIALOGUE_DIR', 'medialogue')

# Look for user function to define file paths
MEDIALOGUE_PATH = getattr(settings, 'MEDIALOGUE_PATH', None)

if MEDIALOGUE_PATH is not None:
    if callable(MEDIALOGUE_PATH):
        get_storage_path = MEDIALOGUE_PATH
    else:
        parts = MEDIALOGUE_PATH.split('.')
        module_name = '.'.join(parts[:-1])
        module = import_module(module_name)
        get_storage_path = getattr(module, parts[-1])
else:
    def get_storage_path(instance, filename):
        fn = unicodedata.normalize('NFKD', force_str(filename)).encode('ascii', 'ignore').decode('ascii')
        return os.path.join(MEDIALOGUE_DIR, '', fn)

class SharedQueries(OrderedModelQuerySet):
    def on_site(self):
        """Return objects linked to the current site only."""
        return self.filter(sites__id=settings.SITE_ID)
    def is_public(self):
        return self.filter(is_public=True)

class SharedQueryManager(models.Manager):

    def get_queryset(self):
        return SharedQueries(self.model, using=self._db)

    def is_public(self):
        return self.get_queryset().is_public()

    def on_site(self):
        return self.get_queryset().on_site()

class MedialogueQueryManager(SharedQueryManager, OrderedModelManager):
    pass


class AutoSlugModel(models.Model):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._slug_src = self.title

    def generate_slug(self):
        self.slug, num_found = _generate_slug(self.title, self.__class__)
        return self.slug

    def save(self, *args, **kwargs):
        logger.info("AutoSlugModel.save called by {}".format(self.__class__))
        slug_src_has_changed = False
        if self._get_pk_val() and (self._slug_src != self.title):
            slug_src_has_changed = True


        if self.slug == '' or slug_src_has_changed:
            self.generate_slug()

        super(AutoSlugModel, self).save(*args, **kwargs)




class Album(AutoSlugModel):
    objects = MedialogueQueryManager()
    date_added = models.DateTimeField(_('date published'), default=now)
    title = models.CharField(
        _('title'),
        max_length=250,
        unique=True,
    )
    slug = models.SlugField(
        _('title slug'),
        unique=True,
        max_length=250,
    )
    description = models.TextField(_('description'), blank=True)
    is_public = models.BooleanField(
        _('is public'),
        default=True,
    )
    sites = models.ManyToManyField(
        Site,
        verbose_name=_('sites'),
        blank=True
    )

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')

    def __str__(self):
        return self.title

    def latest(self, limit=LATEST_LIMIT, public=True):
        if not limit:
            limit = self.media_count()
            if public:
                return self.public()[:limit]
            else:
                return self.media.filter(sites__id=settings.SITE_ID)[:limit]

    def public(self):
        """Return a queryset of all the public media in this album."""
        return self.media.is_public().filter(sites__id=settings.SITE_ID)

    def sample(self, count=None, public=True):
        """Return a sample of media, ordered at random.
        If the 'count' is not specified, it will return a number of media
        limited by the GALLERY_SAMPLE_SIZE setting.
        """
        if not count:
            count = SAMPLE_SIZE
            if count > self.photo_count():
                count = self.photo_count()
                if public:
                    photo_set = self.public()
                else:
                    photo_set = self.media.filter(sites__id=settings.SITE_ID)
                    return random.sample(set(photo_set), count)

    def media_count(self, public=True):
        """Return a count of all the media in this album."""
        if public:
            return self.public().count()
        else:
            return self.media.filter(sites__id=settings.SITE_ID).count()

    media_count.short_description = _('count')

    def public(self):
        """Return a queryset of all the public media in this album."""
        return self.media.is_public().filter(sites__id=settings.SITE_ID)

    def get_absolute_url(self):
        return reverse('medialogue:ml-album', args=[self.slug])

class Media( OrderedModel, AutoSlugModel):
    objects = MedialogueQueryManager()
    album = models.ForeignKey(Album, related_name="media", on_delete=models.CASCADE)
    order_with_respect_to = 'album'

    date_taken = models.DateTimeField(
        _('date taken'),
        null=True,
        blank=True,
    )
    title = models.CharField(
        _('title'),
        max_length=250,
    )
    slug = models.SlugField(
        _('slug'),
        unique=True,
        max_length=250,
    )
    caption = models.TextField(_('caption'), blank=True)
    date_added = models.DateTimeField(_('date added'), default=now)
    is_public = models.BooleanField(
        _('is public'),
        default=True,
    )

    sites = models.ManyToManyField(
        Site,
        verbose_name=_('sites'),
        blank=True,
    )

    def generate_slug(self):
        parent_cls_from_child = next(iter(self._meta.parents))
        self.slug, num_found = _generate_slug(self.title, parent_cls_from_child)
        return self.slug

    def get_previous_in_album(self, album):
        """Find the neighbour of this media object in the supplied album.
        We assume that the album and all its objects are on the same site.
        """
        if not self.is_public:
            raise ValueError('Cannot determine neighbours of a non-public media.')
        media = album.media.is_public()

        # TODO - issues with Photo/Video/Media objects.  self will look like Photo(I) while 
        # The media queryset will look like [Media(I)]
        #if self not in media:
        #    raise ValueError('media does not belong to album.')

        previous = None
        for m in media:
            if m.id == self.id:
                return previous
            previous = m

    def get_next_in_album(self, album):
        """Find the neighbour of this media object in the supplied album.
        We assume that the album and all its objects are on the same site.
        """
        if not self.is_public:
            raise ValueError('Cannot determine neighbours of a non-public media.')
        media = album.media.is_public()
        matched = False

        for m in media:
            if matched:
                return m
            if m.id == self.id:
                matched = True
        return None

    def get_absolute_url(self):
        if hasattr(self, 'video'):
            return self.video.get_absolute_url()
        else:
            return self.photo.get_absolute_url()

    def preview(self):
        if hasattr(self, 'video'):
            return self.video.thumbnail
        else:
            return self.photo.src

class Photo(Media):
    objects = MedialogueQueryManager()
    src = models.ImageField(
        _('src'),
        max_length=IMAGE_FIELD_MAX_LENGTH,
        upload_to=get_storage_path,
    )

    def EXIF(self, file=None):
        try:
            if file:
                tags = exifread.process_file(file)
            else:
                with self.src.storage.open(self.src.name, 'rb') as file:
                    tags = exifread.process_file(file, details=False)
            return tags
        except:
            return {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_src = self.src

    def get_absolute_url(self):
        return reverse('medialogue:ml-photo', args=[self.slug])

    def save(self, *args, **kwargs):
        logger.debug("Photo.save called")
        image_has_changed = False
        if self._get_pk_val() and (self._old_src != self.src):
            image_has_changed = True
            self._old_src.storage.delete(self._old_src.name)  # Delete (old) base image.

        if self.date_taken is None or image_has_changed:
            # Attempt to get the date the photo was taken from the EXIF data.
            try:
                exif_date = self.EXIF(self.src.file).get('EXIF DateTimeOriginal', None)
                if exif_date is not None:
                    d, t = exif_date.values.split()
                    year, month, day = d.split(':')
                    hour, minute, second = t.split(':')
                    self.date_taken = datetime(int(year), int(month), int(day),
                                 int(hour), int(minute), int(second))
            except:
                logger.error('Failed to read EXIF DateTimeOriginal', exc_info=True)
        super(Photo, self).save(*args, **kwargs)

class Video(Media):
    """
    NOTE -  Calls post_save connected in apps.py/signals.py
    - medialogue.tasks.create_thumbnail 
    - django_video_encoding.tasks.convert_all_videos
    """
    objects = MedialogueQueryManager()
    thumbnail = models.ImageField(blank=True)
    format_set = GenericRelation(Format)
    # video detail fields
    width = models.PositiveIntegerField(editable=False, null=True)
    height = models.PositiveIntegerField(editable=False, null=True)
    duration = models.FloatField(editable=False, null=True)
    src = VideoField(
        width_field='width',
        height_field='height',
        duration_field='duration'
    )

    def get_absolute_url(self):
        return reverse("medialogue:ml-video", args=[self.slug])

    def __str__(self):
        return self.title



def add_default_site(instance, created, **kwargs):
    """
    Called via Django's signals when an instance is created.
    In case PHOTOLOGUE_MULTISITE is False, the current site (i.e.
    ``settings.SITE_ID``) will always be added to the site relations if none are
    present.
    """
    if not created:
        return
    if getattr(settings, 'MEDIALOGUE_MULTISITE', False):
        return
    if instance.sites.exists():
        return
    instance.sites.add(Site.objects.get_current())


post_save.connect(add_default_site, sender=Album)
post_save.connect(add_default_site, sender=Video)
post_save.connect(add_default_site, sender=Photo)
