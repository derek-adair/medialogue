import os
from django.test import TestCase, Client
import pytest

from medialogue.forms import *
from medialogue.models import Photo

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

    def test_new_album_form_cleans_the_filepond_input(self):
        form = NewAlbumForm(self.min_gallery)

        form.is_valid()

        self.assertEqual(self.min_gallery['filepond'], form.cleaned_data['filepond'])

    def test_new_album_form_can_take_more_than_one_filepond_input(self):
        form = NewAlbumForm(self.multi_file_gallery)

        form.is_valid()

        self.assertEqual(self.multi_file_gallery['filepond'], form.cleaned_data['filepond'])

    #@pytest.mark.db
    #def test_bulk_media_form_throws_an_error_on_duplicate_gallery_name(self):
    #    form1 = NewAlbumForm(self.min_gallery)
    #    form2 = NewAlbumForm(self.min_gallery)
    #    if form1.is_valid():
    #        form1.save()
    #    if form2.is_valid():
    #        form2.save()

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
