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
from medialogue.forms import _generate_slug, MediaForm

from medialogue.utils import querydict_to_dict

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

    post_data = querydict_to_dict(request.data)
    form = MediaForm(post_data or None)

    if form.is_valid():
        album = form.save(album=album)
        return Response({"msg":"added to album", "redirect_url": album.get_absolute_url() }, status=status.HTTP_200_OK)
    else:
        return Response({"msg" : "Invalid Form"}, status=status.HTTP_400_BAD_REQUEST)
