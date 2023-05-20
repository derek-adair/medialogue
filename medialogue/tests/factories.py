# coding=utf-8

import datetime
import os

from django.conf import settings
from django.utils.text import slugify
from django.utils.timezone import utc

# Temp File Stuff
from django.core.files.uploadedfile import SimpleUploadedFile
from django_drf_filepond.models import TemporaryUpload
from django_drf_filepond.utils import _get_file_id

try:
    import factory
except ImportError:
    raise ImportError(
        "No module named factory. To run medialogue's tests you need to install factory-boy.")

from medialogue.models import Album, Photo

RES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
LANDSCAPE_IMAGE_PATH = os.path.join(RES_DIR, 'test_medialogue_landscape.jpg')

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

class TemporyUploadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TemporaryUpload

    img_bytes = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;'
    file_name = 'tiny.gif'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        upload_id = _get_file_id()
        file_id = _get_file_id()
        uploaded_file = SimpleUploadedFile(cls.file_name, cls.img_bytes, content_type="image/gif")

        temp_upload = TemporaryUpload(
            upload_id=upload_id,
            file_id=file_id,
            file=uploaded_file, upload_name=cls.file_name,
            upload_type=TemporaryUpload.FILE_DATA
        )
        temp_upload.save()
        return temp_upload
