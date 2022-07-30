import unittest

from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase, override_settings

from .factories import AlbumFactory, PhotoFactory
from medialogue.models import Media


@override_settings(ROOT_URLCONF='medialogue.tests.test_urls')
class SitesTest(TestCase):

    def setUp(self):
        """
        Create two example sites that we can use to test what gets displayed
        where.
        """
        super(SitesTest, self).setUp()

        self.site1, created1 = Site.objects.get_or_create(
            domain="example.com", name="example.com")
        self.site2, created2 = Site.objects.get_or_create(
            domain="example.org", name="example.org")

        with self.settings(MEDIALOGUE_MULTISITE=True):
            # Be explicit about linking Albums/Photos to Sites."""
            self.album1 = AlbumFactory(slug='test-album', sites=[self.site1])
            self.album2 = AlbumFactory(slug='not-on-site-album')
            self.photo1 = PhotoFactory(slug='test-photo', sites=[self.site1], album=self.album1)
            self.photo2 = PhotoFactory(slug='not-on-site-photo', album=self.album1)

        # I'd like to use factory_boy's mute_signal decorator but that
        # will only available once factory_boy 2.4 is released. So long
        # we'll have to remove the site association manually
        self.photo2.sites.clear()

    def tearDown(self):
        super(SitesTest, self).tearDown()
        self.photo1.src.delete()
        self.photo2.src.delete()
        self.album1.delete()
        self.album2.delete()

    def test_basics(self):
        """ See if objects were added automatically (by the factory) to the current site. """
        self.assertEqual(list(self.album1.sites.all()), [self.site1])
        self.assertEqual(list(self.photo1.sites.all()), [self.site1])

    def test_auto_add_sites(self):
        """
        Objects should not be automatically associated with a particular site when
        ``MEDIALOGUE_MULTISITE`` is ``True``.
        """

        with self.settings(MEDIALOGUE_MULTISITE=False):
            album = AlbumFactory()
            photo = PhotoFactory(album=album)
        self.assertEqual(list(album.sites.all()), [self.site1])
        self.assertEqual(list(photo.sites.all()), [self.site1])

        photo.src.delete()

        with self.settings(MEDIALOGUE_MULTISITE=True):
            album = AlbumFactory()
            photo = PhotoFactory(album=album)
        self.assertEqual(list(album.sites.all()), [])
        self.assertEqual(list(photo.sites.all()), [])
        photo.src.delete()


    def test_album_list(self):
        response = self.client.get('/ptests/albums/')
        self.assertEqual(list(response.context['object_list']), [self.album1])

    def test_album_detail(self):
        response = self.client.get('/ptests/album/test-album/')
        self.assertEqual(response.context['object'], self.album1)

        response = self.client.get('/ptests/album/not-on-site-album/')
        self.assertEqual(response.status_code, 404)

    def test_photo_list(self):
        response = self.client.get('/ptests/photos/')
        self.assertEqual(list(response.context['object_list']), [self.photo1])

    def test_photo_detail(self):
        response = self.client.get('/ptests/photo/test-photo/')
        self.assertEqual(response.context['object'], self.photo1)

        response = self.client.get('/ptests/photo/not-on-site-photo/')
        self.assertEqual(response.status_code, 404)

    def test_photos_in_album(self):
        """
        Only those photos are supposed to be shown in a album that are
        also associated with the current site.
        """
        response = self.client.get('/ptests/album/test-album/')

        self.assertEqual(list(response.context['object'].public()), [self.photo1.media_ptr])
