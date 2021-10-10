from django.test import TestCase

from medialogue.forms import BulkMediaForm

class BulkMediaFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # @WARNING - VERY fragile test, filepond input represents a list of temporary files stored by
        #       filepond, which is in `filepond-temp-uploads` by default and configured by the
        #       "DJANGO_DRF_FILEPOND_UPLOAD_TMP" setting.
        #        @TODO - this should probably all be mocked? ¯\_(**)_/¯
        cls.min_gallery = minimum_gallery = {'gallery_title': 'some gallery', 'filepond': ['enRqzReaCQSMEb2nFX9hmq']}

    def test_bulk_media_form_cleans_the_filepond_input(self):
        form = BulkMediaForm(self.min_gallery)

        form.is_valid()

        self.assertEqual(self.min_gallery['filepond'], form.cleaned_data['filepond'])
