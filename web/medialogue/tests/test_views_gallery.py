from django.test import TestCase, override_settings

from .factories import AlbumFactory


@override_settings(ROOT_URLCONF='medialogue.tests.test_urls')
class RequestAlbumTest(TestCase):

    def setUp(self):
        super(RequestAlbumTest, self).setUp()
        self.gallery = AlbumFactory(slug='test-gallery')

    def test_paginated_gallery_url_works(self):
        response = self.client.get('/ptests/gallerylist/')
        self.assertEqual(response.status_code, 200)

    def test_gallery_works(self):
        response = self.client.get('/ptests/gallery/test-gallery/')
        self.assertEqual(response.status_code, 200)

    def test_detail_gallery_works(self):
        response = self.client.get('/ptests/gallery/2011/12/23/test-gallery/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_list(self):
        """Trivial test - if someone requests the root url of the app
        (i.e. /ptests/'), redirect them to the gallery list page."""
        response = self.client.get('/ptests/')
        self.assertRedirects(response, '/ptests/gallery/', 301, 200)
