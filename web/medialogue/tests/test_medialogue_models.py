from django.test import TestCase, Client
import pytest
from medialogue.models import Video
from medialogue.forms import MediaForm

from .factories import (LANDSCAPE_IMAGE_PATH, NONSENSE_IMAGE_PATH, QUOTING_IMAGE_PATH, UNICODE_IMAGE_PATH,
                        AlbumFactory, PhotoFactory)

#class MediaModelFormTest(TestCase):
#    def setUp(self): 
#        super(MediaModelFormTest, self).setUp()
#        self.p1 = PhotoFactory()
#
#    def test_form_can_save_a_photo(self):
#        form = MediaForm()
#        form.save()
class MediaModelTest(TestCase):
    pass
