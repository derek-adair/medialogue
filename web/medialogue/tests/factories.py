# coding=utf-8

import datetime
import os

from django.conf import settings
from django.utils.text import slugify
from django.utils.timezone import utc

try:
    import factory
except ImportError:
    raise ImportError(
        "No module named factory. To run medialogue's tests you need to install factory-boy.")

from medialogue.models import Album, Photo

RES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
LANDSCAPE_IMAGE_PATH = os.path.join(RES_DIR, 'test_medialogue_landscape.jpg')
PORTRAIT_IMAGE_PATH = os.path.join(RES_DIR, 'test_medialogue_portrait.jpg')
SQUARE_IMAGE_PATH = os.path.join(RES_DIR, 'test_medialogue_square.jpg')
QUOTING_IMAGE_PATH = os.path.join(RES_DIR, 'test_medialogue_&quoting.jpg')
UNICODE_IMAGE_PATH = os.path.join(RES_DIR, 'test_unicode_®.jpg')
NONSENSE_IMAGE_PATH = os.path.join(RES_DIR, 'test_nonsense.jpg')
SAMPLE_ZIP_PATH = os.path.join(RES_DIR, 'zips/sample.zip')
SAMPLE_NOT_IMAGE_ZIP_PATH = os.path.join(RES_DIR, 'zips/not_image.zip')
IGNORED_FILES_ZIP_PATH = os.path.join(RES_DIR, 'zips/ignored_files.zip')


class AlbumFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Album

    title = factory.Sequence(lambda n: 'album{0:0>3}'.format(n))
    slug = factory.LazyAttribute(lambda a: slugify(a.title))

    @factory.sequence
    def date_added(n):
        # Have to cater projects being non-timezone aware.
        if settings.USE_TZ:
            sample_date = datetime.datetime(
                year=2011, month=12, day=23, hour=17, minute=40, tzinfo=utc)
        else:
            sample_date = datetime.datetime(year=2011, month=12, day=23, hour=17, minute=40)
        return sample_date + datetime.timedelta(minutes=n)

    @factory.post_generation
    def sites(self, create, extracted, **kwargs):
        """
        Associates the object with the current site unless ``sites`` was passed,
        in which case the each item in ``sites`` is associated with the object.

        Note that if MEDIALOGUE_MULTISITE is False, all Album/Photos are automatically
        associated with the current site - bear this in mind when writing tests.
        """
        if not create:
            return
        if extracted:
            for site in extracted:
                self.sites.add(site)

class PhotoFactory(factory.django.DjangoModelFactory):

    """Note: after creating Photo instances for tests, remember to manually
    delete them.
    """

    class Meta:
        model = Photo

    title = factory.Sequence(lambda n: 'photo{0:0>3}'.format(n))
    slug = factory.LazyAttribute(lambda a: slugify(a.title))
    src = factory.django.ImageField(from_path=LANDSCAPE_IMAGE_PATH)

    @factory.sequence
    def date_added(n):
        # Have to cater projects being non-timezone aware.
        if settings.USE_TZ:
            sample_date = datetime.datetime(
                year=2011, month=12, day=23, hour=17, minute=40, tzinfo=utc)
        else:
            sample_date = datetime.datetime(year=2011, month=12, day=23, hour=17, minute=40)
        return sample_date + datetime.timedelta(minutes=n)

    @factory.post_generation
    def sites(self, create, extracted, **kwargs):
        """
        Associates the object with the current site unless ``sites`` was passed,
        in which case the each item in ``sites`` is associated with the object.

        Note that if MEDIALOGUE_MULTISITE is False, all Album/Photos are automatically
        associated with the current site - bear this in mind when writing tests.
        """
        if not create:
            return
        if extracted:
            for site in extracted:
                self.sites.add(site)
