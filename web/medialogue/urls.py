from django.urls import path
from .views import GalleryListView, BulkUpload
app_name = 'medialogue'
urlpatterns = [
	path('', GalleryListView.as_view(), name='gallery-list'),
        path('upload/', BulkUpload, name='bulk-upload'),
]
