from django.test import TestCase, override_settings

from .factories import AlbumFactory


@override_settings(ROOT_URLCONF='medialogue.tests.test_urls')
class RequestAlbumTest(TestCase):

    def setUp(self):
        super(RequestAlbumTest, self).setUp()
        self.album = AlbumFactory(slug='test-album')

    def test_album_url_works(self):
        response = self.client.get('/ptests/albums/')
        self.assertEqual(response.status_code, 200)

    def test_detail_album_works(self):
        response = self.client.get('/ptests/album/test-album/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_list(self):
        """Trivial test - if someone requests the root url of the app
        (i.e. /ptests/'), redirect them to the album list page."""
        response = self.client.get('/ptests/')
        self.assertRedirects(response, '/ptests/albums/', 301, 200)
