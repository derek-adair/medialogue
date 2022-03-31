# -*- coding: utf-8 -*-

import os
import unittest
from io import BytesIO
from unittest.mock import patch

from django import VERSION
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from ..models import MEDIALOGUE_DIR, Photo
from .factories import (LANDSCAPE_IMAGE_PATH, NONSENSE_IMAGE_PATH, QUOTING_IMAGE_PATH, UNICODE_IMAGE_PATH,
                        AlbumFactory, PhotoFactory)
from .helpers import MedialogueBaseTest


class PhotoTest(MedialogueBaseTest):

    def tearDown(self):
        """Delete any extra test files (if created)."""
        super(PhotoTest, self).tearDown()
        try:
            self.pl2.delete()
        except:
            pass

    def test_new_photo(self):
        self.assertEqual(Photo.objects.count(), 1)
        self.assertTrue(self.pl.src.storage.exists(self.pl.src.name))
        self.assertEqual(self.pl.src.storage.size(self.pl.src.name),
                         os.path.getsize(LANDSCAPE_IMAGE_PATH))

    # def test_exif(self):
    #    self.assertTrue(len(self.pl.EXIF.keys()) > 0)

    def test_paths(self):
        self.assertEqual(os.path.normpath(str(self.pl.cache_path())).lower(),
                         os.path.normpath(os.path.join(MEDIALOGUE_DIR,
                                                       'photos',
                                                       'cache')).lower())
        self.assertEqual(self.pl.cache_url(),
                         settings.MEDIA_URL + MEDIALOGUE_DIR + '/photos/cache')

    def test_count(self):
        for i in range(5):
            self.pl.get_testPhotoSize_url()
        self.assertEqual(self.pl.view_count, 0)
        self.s.increment_count = True
        self.s.save()
        for i in range(5):
            self.pl.get_testPhotoSize_url()
        self.assertEqual(self.pl.view_count, 5)

    def test_accessor_methods(self):
        self.assertEqual(self.pl.get_testPhotoSize_photosize(), self.s)
        self.assertEqual(self.pl.get_testPhotoSize_size(),
                         Image.open(self.pl.src.storage.open(
                             self.pl.get_testPhotoSize_filename())).size)
        self.assertEqual(self.pl.get_testPhotoSize_url(),
                         self.pl.cache_url() + '/' + self.pl._get_filename_for_size(self.s))
        self.assertEqual(self.pl.get_testPhotoSize_filename(),
                         os.path.join(self.pl.cache_path(),
                                      self.pl._get_filename_for_size(self.s)))

    def test_quoted_url(self):
        """Test for issue #29 - filenames of photos are incorrectly quoted when
        building a URL."""

        # Create a Photo with a name that needs quoting.
        self.pl2 = PhotoFactory(src__from_path=QUOTING_IMAGE_PATH)
        # Quoting method filepath_to_uri has changed in Django 1.9 - so the string that we're looking
        # for depends on the Django version.
        if VERSION[0] == 1 and VERSION[1] <= 8:
            quoted_string = 'test_medialogue_%26quoting_testPhotoSize.jpg'
        else:
            quoted_string = 'test_medialogue_quoting_testPhotoSize.jpg'
        self.assertIn(quoted_string,
                      self.pl2.get_testPhotoSize_url(),
                      self.pl2.get_testPhotoSize_url())

    def test_unicode(self):
        """Trivial check that unicode titles work.
        (I was trying to track down an elusive unicode issue elsewhere)"""
        self.pl2 = PhotoFactory(title='É',
                                slug='é')


class PhotoManagerTest(MedialogueBaseTest):
    """Some tests for the methods on the Photo manager class."""

    def setUp(self):
        """Create 2 photos."""
        super(PhotoManagerTest, self).setUp()
        self.pl2 = PhotoFactory()

    def tearDown(self):
        super(PhotoManagerTest, self).tearDown()
        self.pl2.delete()

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


class ImageModelTest(MedialogueBaseTest):

    def setUp(self):
        super(ImageModelTest, self).setUp()

        # Unicode image has unicode in the path
        # self.pu = TestPhoto(name='portrait')
        self.pu = PhotoFactory()
        self.pu.src.save(os.path.basename(UNICODE_IMAGE_PATH),
                           ContentFile(open(UNICODE_IMAGE_PATH, 'rb').read()))

        # Nonsense image contains nonsense
        # self.pn = TestPhoto(name='portrait')
        self.pn = PhotoFactory()
        self.pn.src.save(os.path.basename(NONSENSE_IMAGE_PATH),
                           ContentFile(open(NONSENSE_IMAGE_PATH, 'rb').read()))

    def tearDown(self):
        super(ImageModelTest, self).tearDown()
        self.pu.delete()
        self.pn.delete()

def raw_image(mode='RGB', fmt='JPEG'):
    """Create raw image.
    """
    data = BytesIO()
    Image.new(mode, (100, 100)).save(data, fmt)
    data.seek(0)
    return data


class ImageTransparencyTest(MedialogueBaseTest):

    def setUp(self):
        super(ImageTransparencyTest, self).setUp()
        self.png = PhotoFactory()
        self.png.src.save(
            'trans.png', ContentFile(raw_image('RGBA', 'PNG').read()))

    def tearDown(self):
        super(ImageTransparencyTest, self).tearDown()
        self.png.clear_cache()
        os.unlink(os.path.join(settings.MEDIA_ROOT, self.png.src.path))

    def test_create_size_png_keep_alpha_channel(self):
        thumbnail = self.png.get_thumbnail_filename()
        im = Image.open(
            os.path.join(settings.MEDIA_ROOT, thumbnail))
        self.assertEqual('RGBA', im.mode)
