import logging
logger = logging.getLogger(__name__)
from io import BytesIO
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

from .models import MediaGallery, Video
from photologue.models import Photo

class BulkMediaForm(forms.Form):
    gallery = forms.ModelChoiceField(MediaGallery.objects.all(),
                                     label=_('Gallery'),
                                     required=False,
                                     help_text=_('Select a gallery to add these images to. Leave this empty to '
                                                 'create a new gallery from the supplied title.'))
    gallery_title = forms.CharField(label='Gallery Title', max_length=100, required=False)

    media_title = forms.CharField(label=_('Default Media Title'),
                            max_length=250,
                            required=False,
                            help_text=_('All uploaded media will be given a title made up of this title + a '
                                        'sequential number.<br>This field is required if creating a new '
                                        'gallery, but is optional when adding to an existing gallery - if '
                                        'not supplied, the photo titles will be creating from the existing '
                                        'gallery name.'))

    description = forms.CharField(label=_('Description'),
                                  required=False,
                                  help_text=_('A description of this Gallery. Only required for new galleries.'))

    is_public = forms.BooleanField(label=_('Is public'),
                                   initial=True,
                                   required=False,
                                   help_text=_('Uncheck this to make the uploaded '
                                               'gallery and included photographs private.'))
    filepond = SimpleArrayField(forms.CharField(max_length=255), widget=forms.HiddenInput(),
            required=False)
    date_added = forms.DateField(widget=AdminDateWidget(), label="Date")

    def clean_title(self):
        gallery_title = self.cleaned_data['gallery_title']
        if gallery_title and MediaGallery.objects.filter(title=gallery_title).exists():
            raise forms.ValidationError(_('A gallery with that title already exists.'))
        return gallery_title

    def clean(self):
        cleaned_data = super().clean()
        if not self['gallery_title'].errors:
            # If there's already an error in the title, no need to add another
            # error related to the same field.
            if not cleaned_data.get('gallery_title', None) and not cleaned_data['gallery']:
                raise forms.ValidationError(
                    _('Select an existing gallery, or enter a title for a new gallery.'))
        return cleaned_data

    def _generate_slug(self, title):
        slug_candidate = slug_original = slugify(title)
        num_found = 0
        for i in itertools.count(1):
            if not Photo.objects.filter(slug=slug_candidate).exists() and not Video.objects.filter(slug=slug_candidate).exists():
                break
            num_found+=1
            slug_candidate = '{}-{}'.format(slug_original, i)
        return slug_candidate, num_found

    def save(self):
        filelist = self.cleaned_data['filepond']

        current_site = Site.objects.get(id=settings.SITE_ID)
        if self.cleaned_data['gallery']:
            logger.debug('Using pre-existing gallery.')
            gallery = self.cleaned_data['gallery']
        else:
            logger.debug('Creating new gallery "{0}".'.format(self.cleaned_data['gallery_title']))
            gallery = MediaGallery.objects.create(title=self.cleaned_data['gallery_title'],
                                             date_added=self.cleaned_data['date_added'],
                                             slug=slugify(self.cleaned_data['gallery_title']),
                                             description=self.cleaned_data['description'],
                                             is_public=self.cleaned_data['is_public'])
            gallery.sites.add(current_site)

	# This is where we diverge from photologue 
	# Here we are reading a list of filepond IDS which we will then import
	# via store_upload from drf-filepond: https://tinyurl.com/3t3623b2
        for upload_id in filelist:
            logger.debug('Reading file "{}".'.format(upload_id))

            su = store_upload(upload_id,
                    destination_file_path="photologue/{}".format(upload_id))

            (filename, data) = get_stored_upload_file_data(su)
            if not len(data):
                logger.debug('File "{}" is empty.'.format(filename))
                continue

            media_title_root = numbered_title = self.cleaned_data['media_title'] if self.cleaned_data['media_title'] else gallery.title

            # A photo might already exist with the same slug. So it's somewhat inefficient,
            # but we loop until we find a slug that's available.
            slug, num_found = self._generate_slug(media_title_root)

            if num_found > 0:
                numbered_title = "{}({})".format(media_title_root, num_found)

            file_mimetype = magic.from_buffer(data, mime=True).split('/')[0]
            if file_mimetype  == 'image':
                logger.info("image mimetype detected")
                photo = Photo(title=numbered_title,
                              slug=slug,
                              date_added=self.cleaned_data['date_added'],
                              is_public=self.cleaned_data['is_public'])

                photo.image = "photologue/{}".format(upload_id)
                photo.save()
                photo.sites.add(current_site)
                gallery.photos.add(photo)
            elif file_mimetype == "video":
                logger.info("video mimetype detected")
                video = Video(title=numbered_title, slug=slug, date_added=self.cleaned_data['date_added'], is_public=self.cleaned_data['is_public'])
                video.file = "photologue/{}".format(upload_id)
                video.save()
                gallery.videos.add(video)
            else:
                logger.error('cound not process file "{}"'.format(filename))
        return gallery.slug
