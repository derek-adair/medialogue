from django.core.files import File
from video_encoding.backends import get_backend
import os

import logging
logger = logging.getLogger(__name__)

from .models import Video

def create_thumbnail(video_pk):
    logger.info("create_thumbnail task called")
    video = Video.objects.get(pk=video_pk)
    if not video.file:
        # no video file attached
        return

    if video.thumbnail:
        # thumbnail has already been generated
        return

    encoding_backend = get_backend()
    thumbnail_path = encoding_backend.get_thumbnail(video.file.path)
    filename = os.path.basename(thumbnail_path)

    try:
        with open(thumbnail_path, 'rb') as file_handler:
            django_file = File(file_handler)
            video.thumbnail.save(filename, django_file)
        video.save()
    finally:
        os.unlink(thumbnail_path)
