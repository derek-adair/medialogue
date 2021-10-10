from django.test import TestCase

from medialogue.forms import BulkMediaForm

class BulkMediaFormTestCase(TestCase):
    def test_bulk_media_form_cleans_the_filepond_input(self):
        minimum_gallery = {'gallery_title': 'some gallery', 'filepond': ['enRqzReaCQSMEb2nFX9hmq']}
        form = BulkMediaForm(minimum_gallery)

        form.is_valid()

        self.assertEqual(minimum_gallery['filepond'], form.cleaned_data['filepond'])
