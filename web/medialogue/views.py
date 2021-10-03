from django.views.generic.list import ListView
from .models import MediaGallery

def GalleryListView(ListView):
    queryset = MediaGallery.objects.on_site().is_public() 
