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


def _generate_slug(title, obj):
    slug_candidate = slug_original = slugify(title)
    num_found = 0
    for i in itertools.count(1):
        if not obj.objects.filter(slug=slug_candidate).exists() and not Video.objects.filter(slug=slug_candidate).exists():
            break
        num_found+=1
        slug_candidate = '{}-{}'.format(slug_original, i)
    return slug_candidate, num_found

class MediaForm(forms.Form):
    description = forms.CharField(label=_('Description'),
                                  required=False,
                                  help_text=_('A description of this Album. Only required for new albums.'))

    is_public = forms.BooleanField(label=_('Public'),
                                   initial=True,
                                   required=False,
                                   help_text=_('Uncheck this to make the uploaded '
                                               'gallery and included photographs private.'))
    filepond = SimpleArrayField(forms.CharField(max_length=255), widget=forms.HiddenInput(),
           required=False)


    def save(self, gallery):
        filelist = self.cleaned_data['filepond']
        CURRENT_SITE = Site.objects.get(id=settings.SITE_ID)

        # read list of filepond IDS which we will then import
        # via store_upload from drf-filepond: https://tinyurl.com/3t3623b2
        for upload_id in filelist:
            logger.debug('Reading file "{}".'.format(upload_id))

            su = store_upload(upload_id, destination_file_path=upload_id)

            (filename, data) = get_stored_upload_file_data(su)
            if not len(data):
                logger.debug('File "{}" is empty.'.format(filename))
                continue

            media_title_root = numbered_title = gallery.title

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
                        )

                photo.src = "medialogue/{}".format(upload_id)
                photo.save()
                photo.sites.add(CURRENT_SITE)
                gallery.photos.add(photo)
            elif file_mimetype == "video":
                logger.info("video mimetype detected")
                video = Video(title=numbered_title, slug=slug, is_public=self.cleaned_data['is_public'])
                video.src = "medialogue/{}".format(upload_id)
                video.save()
                video.sites.add(CURRENT_SITE)
                gallery.videos.add(video)
            else:
                logger.error('cound not process file "{}"'.format(filename))
        return gallery.slug

class NewAlbumForm(MediaForm):
    gallery_title = forms.CharField(label='Album Title', max_length=100, required=False)

    field_order = ['gallery_title', 'is_public', 'description', 'filepond',]

    def clean_title(self):
        gallery_title = self.cleaned_data['gallery_title']
        if Album.objects.filter(title=gallery_title).exists():
            raise forms.ValidationError(_('A gallery with that title already exists.'))
        return gallery_title

    def save(self):
        CURRENT_SITE = Site.objects.get(id=settings.SITE_ID)
        slug, num_found = _generate_slug(self.cleaned_data['gallery_title'], Album)
        gallery = Album.objects.create(title=self.cleaned_data['gallery_title'],
                                              slug=slug,
                                              description=self.cleaned_data['description'],
                                              is_public=self.cleaned_data['is_public'])
        gallery.sites.add(CURRENT_SITE)
        return super(NewAlbumForm, self).save(gallery)

class EditAlbumForm(MediaForm):
    gallery = forms.ModelChoiceField(Album.objects.all(),
                                     label=_('Album'),
                                     required=True,
                                     help_text=_('Select a gallery to add these images to. Leave this empty to '
                                                 'create a new gallery from the supplied title.'))
