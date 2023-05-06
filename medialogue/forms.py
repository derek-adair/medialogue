import logging
logger = logging.getLogger(__name__)
from io import BytesIO
import datetime
import itertools
import magic
from PIL import Image, UnidentifiedImageError

from django import forms
from django.contrib.postgres.forms.array import SimpleArrayField
from django.contrib.sites.models import Site
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.conf import settings

from django_drf_filepond.api import store_upload, get_stored_upload_file_data
from django_drf_filepond.models import TemporaryUpload

from .models import Album, Video, Photo
from .signals import media_added

from .utils import _generate_slug

class MediaForm(forms.Form):
    """
    Base filepond media form that takes an album, and a list of filepond files to add to said album
    """
    is_public = forms.BooleanField(label=_('Public'),
                                   initial=True,
                                   required=False,
                                 )
    filepond = SimpleArrayField(forms.CharField(max_length=255), widget=forms.HiddenInput(),
           required=False)


    def save(self, album):
        filelist = self.cleaned_data['filepond']
        CURRENT_SITE = Site.objects.get(id=settings.SITE_ID)
        new_media_detected = False

        # read list of filepond IDS which we will then import
        # via store_upload from drf-filepond: https://tinyurl.com/3t3623b2
        for upload_id in filelist:
            logger.debug('Reading file "{}".'.format(upload_id))

            su = store_upload(upload_id, destination_file_path=upload_id)

            (filename, data) = get_stored_upload_file_data(su)
            if not len(data):
                logger.debug('File "{}" is empty.'.format(filename))
                continue

            media_title_root = numbered_title = album.title

            # A photo might already exist with the same slug. So it's somewhat inefficient,
            # but we loop until we find a slug that's available.
            slug, num_found = _generate_slug(media_title_root, Photo)

            if num_found > 0:
                numbered_title = "{}({})".format(media_title_root, num_found)

            file_mimetype = magic.from_buffer(data, mime=True).split('/')[0]
            if file_mimetype  == 'image':
                logger.info("image mimetype detected")
                photo = Photo(
                            title=numbered_title,
                            slug=slug,
                            is_public=self.cleaned_data['is_public'],
                            album=album
                        )

                photo.src = "medialogue/{}".format(upload_id)
                photo.save()
                photo.sites.add(CURRENT_SITE)
            elif file_mimetype == "video":
                logger.info("video mimetype detected")
                video = Video(title=numbered_title, slug=slug, is_public=self.cleaned_data['is_public'], album=album)
                video.src = "medialogue/{}".format(upload_id)
                video.save()
                video.sites.add(CURRENT_SITE)
            else:
                logger.error('cound not process file "{}"'.format(filename))
            new_media_detected = True

        if new_media_detected:
            media_added.send(sender=album.__class__, instance=album)

        return album

class NewAlbumForm(MediaForm):
    """
    Used in /album/new/
    - requires album_title
    - saves a new album for the current site
    - saves a list of filepond files from MediaForm
    """
    description = forms.CharField(label=_('Description'), required=False,)
    album_title = forms.CharField(label='Album Title', max_length=100 )

    field_order = ['album_title', 'is_public', 'description', 'filepond',]

    def clean_title(self):
        album_title = self.cleaned_data['album_title']
        if Album.objects.filter(title=album_title).exists():
            raise forms.ValidationError(_('A album with that title already exists.'))
        return album_title

    def save(self):
        CURRENT_SITE = Site.objects.get(id=settings.SITE_ID)
        slug, num_found = _generate_slug(self.cleaned_data['album_title'], Album)
        album = Album.objects.create(title=self.cleaned_data['album_title'],
                                              slug=slug,
                                              description=self.cleaned_data['description'],
                                              is_public=self.cleaned_data['is_public'])
        album.sites.add(CURRENT_SITE)
        return super(NewAlbumForm, self).save(album)

class EditAlbumForm(forms.ModelForm):
    """
    Used in /album/{ID}/edit/ to edit album meta data
    """
    class Meta:
        model = Album
        fields = ['title', 'description', 'is_public']
