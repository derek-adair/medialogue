import logging
logger = logging.getLogger(__name__)

from django.core.exceptions import ObjectDoesNotExist
from medialogue.models import Media, Album, Photo, Video

from django_drf_filepond.api import store_upload, get_stored_upload_file_data
from django_drf_filepond.models import TemporaryUpload
import magic
from PIL import Image, UnidentifiedImageError

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework import status
from medialogue.forms import _generate_slug

@api_view(['POST'])
def reorder_media(request, pk):
    try:
        media = Media.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    order = request.POST.get('order', None)
    if order is None:
        return Response({"msg" : "order field required in form"}, status=status.HTTP_400_BAD_REQUEST)
    media.to(int(order))
    media.save()
    return Response({"msg":"{0} moved to {1}".format(media.title, request.data['order'])},
                    status=status.HTTP_200_OK)

@api_view(['POST'])
def add_to_album(request, pk):
    try:
        album = Album.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    #@TODO - refucktor this to be dry, this is duplicated in the new album form save method
    for upload_id in request.data.getlist('filelist'):

        su = store_upload(upload_id, destination_file_path=upload_id)

        (filename, data) = get_stored_upload_file_data(su)
        if not len(data):
            logger.debug('File "{}" is empty.'.format(filename))
            continue

        media_title_root = numbered_title = album.title

        # A photo might already exist with the same slug. So it's somewhat inefficient,
        # but we loop until we find a slug that's available.
        slug, num_found = _generate_slug(media_title_root, Photo)

        if num_found > 0:
            numbered_title = "{}({})".format(media_title_root, num_found)

        file_mimetype = magic.from_buffer(data, mime=True).split('/')[0]
        if file_mimetype  == 'image':
            logger.info("image mimetype detected")
            photo = Photo(
                        title=numbered_title,
                        slug=slug,
                        is_public=album.is_public,
                    )

            photo.src = "medialogue/{}".format(upload_id)
            photo.album = album
            photo.save()
        elif file_mimetype == "video":
            logger.info("video mimetype detected")
            video = Video(title=numbered_title, slug=slug, is_public=album.is_public)
            video.src = "medialogue/{}".format(upload_id)
            video.album = album
            video.save()
        else:
            logger.error('cound not process file "{}"'.format(filename))
    return Response({"msg":"add_to_album called", "slug": album.slug }, status=status.HTTP_200_OK)
