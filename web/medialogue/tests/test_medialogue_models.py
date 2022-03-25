from django.test import TestCase, Client
import pytest
from .models import Video
class MediaModelTest(TestCase):
    @classmethod
    Video.objects.create(
