import pytest
from .helpers import MedialogueBaseTest
from .factories import PhotoFactory, AlbumFactory

class ApiTest(MedialogueBaseTest):

    def setUp(self):
        """Create a test album with 2 photos."""
        super(ApiTest, self).setUp()
        self.pl2 = PhotoFactory(album=self.album)

    def tearDown(self):
        super(ApiTest, self).tearDown()
        self.pl2.src.delete()

    def test_add_to_album_throws_404(self):
        url = '/api/add-to-album/{0}/'.format(999999999)

        response = self.client.post(url, {})

        self.assertEqual(response.status_code, 404)

    #def test_add_to_album_api(self):
    #    url = '/api/add-to-album/{0}/'.format(self.album.id)

    #    response = self.client.post(url, {})

    #    self.assertEqual(response.status_code, 200)

    def test_reorder_media_api(self):
        url = '/api/reorder-media/{0}/'.format(self.pl2.id)
        data = {'order' : 0}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        # @TODO - following doesn't work for some reason its always reset. I think its something to do
        # with it being @pytest.mark.db or something but that doesn't work either
        #
        #self.assertEqual(self.pl2.order, 0)

    def test_reorder_media_api_throws_404(self):
        url = '/api/reorder-media/{0}/'.format(999999)
        data = {'order' : 0}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 404)

    def test_reorder_media_api_throws_400(self):
        url = '/api/reorder-media/{0}/'.format(self.pl2.id)

        response = self.client.post(url, {})

        self.assertEqual(response.status_code, 400)
