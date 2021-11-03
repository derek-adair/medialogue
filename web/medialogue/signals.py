import logging
logger = logging.getLogger(__name__)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rq import enqueue
from .models import Video
from video_encoding import tasks
from .tasks import create_thumbnail

@receiver(post_save, sender=Video)
def convert_video(sender, instance, **kwargs):
    logger.info('convert_video signal called')
    enqueue(tasks.convert_all_videos,
            instance._meta.app_label,
            instance._meta.model_name,
            instance.pk)

@receiver(post_save, sender=Video)
def thumbnail_signal(sender, instance, **kwargs):
    enqueue(create_thumbnail, instance.pk)
