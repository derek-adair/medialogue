from .. import models
from .factories import AlbumFactory, PhotoFactory
from .helpers import MedialogueBaseTest


class AlbumTest(MedialogueBaseTest):

    def setUp(self):
        """Create a test album with 2 photos."""
        super(AlbumTest, self).setUp()
        self.pl2 = PhotoFactory(album=self.album)

    def tearDown(self):
        super(AlbumTest, self).tearDown()
        self.pl2.src.delete()

    def test_public(self):
        """Method 'public' should only return photos flagged as public."""
        self.assertEqual(self.album.public().count(), 2)
        self.pl.is_public = False
        self.pl.save()
        self.assertEqual(self.album.public().count(), 1)

    def test_media_count(self):
        """Method 'media_count' should return the count of the photos in this
        album."""
        self.assertEqual(self.album.media_count(), 2)
        self.pl.is_public = False
        self.pl.save()
        self.assertEqual(self.album.media_count(), 1)

        # Method takes an optional 'public' kwarg.
        self.assertEqual(self.album.media_count(public=False), 2)

    #def test_sample(self):
    #    """Method 'sample' should return a random queryset of photos from the
    #    album."""

    #    # By default we return all photos from the album (but ordered at random).
    #    _current_sample_size = models.SAMPLE_SIZE
    #    models.SAMPLE_SIZE = 5
    #    self.assertEqual(len(self.album.sample()), 2)

    #    # We can state how many photos we want.
    #    self.assertEqual(len(self.album.sample(count=1)), 1)

    #    # If only one photo is public then the sample cannot have more than one
    #    # photo.
    #    self.pl.is_public = False
    #    self.pl.save()
    #    self.assertEqual(len(self.album.sample(count=2)), 1)

    #    self.pl.is_public = True
    #    self.pl.save()

    #    # We can limit the number of photos by changing settings.
    #    models.SAMPLE_SIZE = 1
    #    self.assertEqual(len(self.album.sample()), 1)

    #    models.SAMPLE_SIZE = _current_sample_size
