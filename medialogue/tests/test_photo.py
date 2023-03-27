# -*- coding: utf-8 -*-

import os
import unittest
from io import BytesIO
from unittest.mock import patch

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from ..models import MEDIALOGUE_DIR, Photo
from PIL import Image
from .factories import (LANDSCAPE_IMAGE_PATH, AlbumFactory, PhotoFactory)
from .helpers import MedialogueBaseTest


class PhotoTest(MedialogueBaseTest):

    def tearDown(self):
        """Delete any extra test files (if created)."""
        super(PhotoTest, self).tearDown()
        try:
            self.pl2.src.delete()
        except:
            pass

    def test_new_photo(self):
        self.assertEqual(Photo.objects.count(), 1)
        self.assertTrue(self.pl.src.storage.exists(self.pl.src.name))
        self.assertEqual(self.pl.src.storage.size(self.pl.src.name),
                         os.path.getsize(LANDSCAPE_IMAGE_PATH))

    #@TODO - Fix test
    #def test_exif(self):
    #    self.assertTrue(len(self.pl.EXIF.keys()) > 0)


    #@TODO - Fix test
    #def test_count(self):
    #    for i in range(5):
    #        self.pl.get_testPhotoSize_url()
    #    self.assertEqual(self.pl.view_count, 0)
    #    self.s.increment_count = True
    #    self.s.save()
    #    for i in range(5):
    #        self.pl.get_testPhotoSize_url()
    #    self.assertEqual(self.pl.view_count, 5)

    #def test_quoted_url(self):
    #    """Test for issue #29 - filenames of photos are incorrectly quoted when
    #    building a URL."""

    #    # Create a Photo with a name that needs quoting.
    #    self.pl2 = PhotoFactory(src__from_path=QUOTING_IMAGE_PATH)
    #    quoted_string = 'test_medialogue_quoting_testPhotoSize.jpg'
    #    self.assertIn(quoted_string,
    #                  self.pl2.get_testPhotoSize_url(),
    #                  self.pl2.get_testPhotoSize_url())

    def test_unicode(self):
        """Trivial check that unicode titles work.
        (I was trying to track down an elusive unicode issue elsewhere)"""
        self.pl2 = PhotoFactory(title='É', slug='é', album=self.album)


class PhotoManagerTest(MedialogueBaseTest):
    """Some tests for the methods on the Photo manager class."""

    def setUp(self):
        """Create 2 photos."""
        super(PhotoManagerTest, self).setUp()
        self.pl2 = PhotoFactory(album=self.album)

    def tearDown(self):
        super(PhotoManagerTest, self).tearDown()
        self.pl2.src.delete()

    def test_public(self):
        """Method 'is_public' should only return photos flagged as public."""
        self.assertEqual(Photo.objects.is_public().count(), 2)
        self.pl.is_public = False
        self.pl.save()
        self.assertEqual(Photo.objects.is_public().count(), 1)


#class PreviousNextTest(MedialogueBaseTest):
#    """Tests for the methods that provide the previous/next photos in a gallery."""
#
#    def setUp(self):
#        """Create a test gallery with 2 photos."""
#        super(PreviousNextTest, self).setUp()
#        self.test_gallery = AlbumFactory()
#        self.pl1 = PhotoFactory()
#        self.pl2 = PhotoFactory()
#        self.pl3 = PhotoFactory()
#        self.test_gallery.photos.add(self.pl1)
#        self.test_gallery.photos.add(self.pl2)
#        self.test_gallery.photos.add(self.pl3)
#
#    def tearDown(self):
#        super(PreviousNextTest, self).tearDown()
#        self.pl1.delete()
#        self.pl2.delete()
#        self.pl3.delete()
#
#    def test_previous_simple(self):
#        # Previous in gallery.
#        self.assertEqual(self.pl1.get_previous_in_gallery(self.test_gallery),
#                         None)
#        self.assertEqual(self.pl2.get_previous_in_gallery(self.test_gallery),
#                         self.pl1)
#        self.assertEqual(self.pl3.get_previous_in_gallery(self.test_gallery),
#                         self.pl2)
#
#    def test_previous_public(self):
#        """What happens if one of the photos is not public."""
#        self.pl2.is_public = False
#        self.pl2.save()
#
#        self.assertEqual(self.pl1.get_previous_in_gallery(self.test_gallery),
#                         None)
#        self.assertRaisesMessage(ValueError,
#                                 'Cannot determine neighbours of a non-public photo.',
#                                 self.pl2.get_previous_in_gallery,
#                                 self.test_gallery)
#        self.assertEqual(self.pl3.get_previous_in_gallery(self.test_gallery),
#                         self.pl1)
#
#    def test_previous_gallery_mismatch(self):
#        """Photo does not belong to the gallery."""
#        self.pl4 = PhotoFactory()
#
#        self.assertRaisesMessage(ValueError,
#                                 'Photo does not belong to gallery.',
#                                 self.pl4.get_previous_in_gallery,
#                                 self.test_gallery)
#
#        self.pl4.delete()
#
#    def test_next_simple(self):
#        # Next in gallery.
#        self.assertEqual(self.pl1.get_next_in_gallery(self.test_gallery),
#                         self.pl2)
#        self.assertEqual(self.pl2.get_next_in_gallery(self.test_gallery),
#                         self.pl3)
#        self.assertEqual(self.pl3.get_next_in_gallery(self.test_gallery),
#                         None)
#
#    def test_next_public(self):
#        """What happens if one of the photos is not public."""
#        self.pl2.is_public = False
#        self.pl2.save()
#
#        self.assertEqual(self.pl1.get_next_in_gallery(self.test_gallery),
#                         self.pl3)
#        self.assertRaisesMessage(ValueError,
#                                 'Cannot determine neighbours of a non-public photo.',
#                                 self.pl2.get_next_in_gallery,
#                                 self.test_gallery)
#        self.assertEqual(self.pl3.get_next_in_gallery(self.test_gallery),
#                         None)
#
#    def test_next_gallery_mismatch(self):
#        """Photo does not belong to the gallery."""
#        self.pl4 = PhotoFactory()
#
#        self.assertRaisesMessage(ValueError,
#                                 'Photo does not belong to gallery.',
#                                 self.pl4.get_next_in_gallery,
#                                 self.test_gallery)
#
#        self.pl4.delete()
