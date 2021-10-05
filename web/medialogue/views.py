from django.views.generic.list import ListView
from .models import MediaGallery

class GalleryListView(ListView):
    queryset = MediaGallery.objects.is_public()
