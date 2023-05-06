import os
import io

import pytest
from PIL import Image
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from django_drf_filepond.models import TemporaryUpload
from django_drf_filepond.utils import _get_file_id

from medialogue.forms import *
from medialogue.models import Photo

class BulkMediaFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
	#Fake the filepond file uplaod
        cls.upload_id = _get_file_id()
        cls.file_id = _get_file_id()
        cls.file_name = "tiny.gif"
        cls.img_bytes = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;'

        uploaded_file = SimpleUploadedFile(cls.file_name, cls.img_bytes, content_type="image/gif")
        temp_upload = TemporaryUpload(
                upload_id=cls.upload_id,
                file_id=cls.file_id,
                file=uploaded_file, upload_name=cls.file_name,
                upload_type=TemporaryUpload.FILE_DATA
            )
        temp_upload.save()

        cls.min_gallery = minimum_gallery = {'album_title': 'some gallery', 'filepond': [cls.upload_id]}
        cls.multi_file_gallery = minimum_gallery = {'album_title': 'some gallery', 'filepond': ['enRqzReaCQSMEb2nFX9hmq', 'enRqzReaCQSMEb2nFX9zzz']}

    def test_new_album_form_cleans_the_filepond_input(self):
        form = NewAlbumForm(self.min_gallery)

        form.is_valid()

        self.assertEqual(self.min_gallery['filepond'], form.cleaned_data['filepond'])

    def test_new_album_form_can_take_more_than_one_filepond_input(self):
        form = NewAlbumForm(self.multi_file_gallery)

        form.is_valid()

        self.assertEqual(self.multi_file_gallery['filepond'], form.cleaned_data['filepond'])

    def test_new_album_form_saves_a_drf_temp_file_to_Photo(self):
        form = NewAlbumForm(self.min_gallery)

        form.is_valid()
        form.save()

        self.assertEqual(os.path.basename(Photo.objects.first().src.name),
                self.min_gallery['filepond'][0])
