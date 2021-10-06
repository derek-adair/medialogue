from django import forms
from django.utils.translation import gettext_lazy as _

from .models import MediaGallery, Video
from photologue.models import Photo

class BulkMediaForm(forms.Form):
    gallery_title = forms.CharField(label='Gallery Title', max_length=100, required=False)
    gallery = forms.ModelChoiceField(MediaGallery.objects.all(),
                                     label=_('Gallery'),
                                     required=False,
                                     help_text=_('Select a gallery to add these images to. Leave this empty to '
                                                 'create a new gallery from the supplied title.'))

    media_title = forms.CharField(label=_('Default Media Title'),
                            max_length=250,
                            required=False,
                            help_text=_('All uploaded photos will be given a title made up of this title + a '
                                        'sequential number.<br>This field is required if creating a new '
                                        'gallery, but is optional when adding to an existing gallery - if '
                                        'not supplied, the photo titles will be creating from the existing '
                                        'gallery name.'))

    is_public = forms.BooleanField(label=_('Is public'),
                                   initial=True,
                                   required=False,
                                   help_text=_('Uncheck this to make the uploaded '
                                               'gallery and included photographs private.'))

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
