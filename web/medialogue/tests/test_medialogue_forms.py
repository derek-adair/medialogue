import os
from django.test import TestCase, Client
import pytest

from medialogue.forms import BulkMediaForm
from photologue.models import Photo

class BulkMediaFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # @WARNING - VERY fragile test, filepond input represents a list of temporary files stored by
        #       filepond, which is in `filepond-temp-uploads` by default and configured by the
        #       "DJANGO_DRF_FILEPOND_UPLOAD_TMP" setting.
        #        @TODO - this should probably all be mocked? ¯\_(**)_/¯
        cls.min_gallery = minimum_gallery = {'gallery_title': 'some gallery', 'filepond': ['enRqzReaCQSMEb2nFX9hmq']}
        cls.multi_file_gallery = minimum_gallery = {'gallery_title': 'some gallery', 'filepond':
                ['enRqzReaCQSMEb2nFX9hmq', 'enRqzReaCQSMEb2nFX9zzz']}

    def test_bulk_media_form_cleans_the_filepond_input(self):
        form = BulkMediaForm(self.min_gallery)

        form.is_valid()

        self.assertEqual(self.min_gallery['filepond'], form.cleaned_data['filepond'])

    def test_bulk_media_form_can_take_more_than_one_filepond_input(self):
        form = BulkMediaForm(self.multi_file_gallery)

        form.is_valid()

        self.assertEqual(self.multi_file_gallery['filepond'], form.cleaned_data['filepond'])

    #@pytest.mark.django_db
    #def test_bulk_media_form_throws_an_error_on_duplicate_gallery_name(self):
    #    form1 = BulkMediaForm(self.min_gallery)
    #    form2 = BulkMediaForm(self.min_gallery)
    #    if form1.is_valid():
    #        form1.save()
    #    if form2.is_valid():
    #        form2.save()
    #    import pdb; pdb.set_trace()

    def test_bulk_media_form_requires_either_gallery_title_or_gallery_fk(self):
        form = BulkMediaForm({'description':'an invalid form'})

        self.assertEqual(form.is_valid(), False)
        self.assertEqual('Select an existing gallery, or enter a title for a new gallery.' in
                form.errors["__all__"], True)

    #def test_bulk_media_form_increments_title_slugs(self):
    #    self.assertEqual('finish test', '')

    #def test_bulk_media_form_saves_a_drf_temp_file_to_Photo(self):
    #    form = BulkMediaForm(self.multi_file_gallery)

    #    form.is_valid()
    #    form.save()

    #    self.assertEqual(os.path.basename(Photo.objects.first().image.name),
    #            self.min_gallery['filepond'][0])

class BulkUploadViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
