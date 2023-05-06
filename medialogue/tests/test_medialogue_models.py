import pytest

from django.test import TestCase, Client

from medialogue.models import Album, Photo, Video
from medialogue.forms import MediaForm

from .factories import (LANDSCAPE_IMAGE_PATH, AlbumFactory, PhotoFactory)

class AlbumModelTest(TestCase):
    def test_slug_is_auto_populated(self):
        album = Album(title="test title")

        album.save()

        self.assertEqual("test-title", album.slug)

class MediaModelTest(TestCase):
    def test_slug_changes_with_title(self):
        album = AlbumFactory()

        photo = Photo(title="test title", album=album)
        photo.save()

        photo.title="A TEST title"

        photo.save()

        self.assertEqual("a-test-title", photo.slug)

    def test_slug_is_auto_populated(self):
        album = AlbumFactory()
        video = Video(title="test title", album=album )

        video.save()

        self.assertEqual("test-title", video.slug)

    def test_photo_and_video_slug_are_unique_together(self):
        #photos and videos can have the same title...
        #  but the slug must been unique between the two
        album = AlbumFactory()
        video = Video(title="test title", album=album )
        photo = Photo(title="test title", album=album )

        video.save()
        photo.save()

        self.assertNotEqual(video.slug, photo.slug)


class PhotoModelTest(TestCase):
    def test_slug_is_auto_populated(self):
        album = AlbumFactory()
        photo = Photo(title="test title", album=album)

        photo.save()

        self.assertEqual("test-title", photo.slug)
