from django.test import TestCase, Client
import pytest
from medialogue.models import Album
from medialogue.forms import MediaForm

from .factories import (LANDSCAPE_IMAGE_PATH, AlbumFactory, PhotoFactory)

class MediaModelTest(TestCase):
    def test_slug_is_auto_populated(self):
        album = Album(title="test title")

        album.save()

        self.assertEqual("test-title", album.slug)
