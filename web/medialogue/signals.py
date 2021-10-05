from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rq import enqueue
from .models import Video
from video_encoding import tasks

@receiver(post_save, sender=Video)
def convert_video(sender, instance, **kwargs):
    enqueue(tasks.convert_all_videos,
            instance._meta.app_label,
            instance._meta.model_name,
            instance.pk)
