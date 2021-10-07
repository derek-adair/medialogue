from django.urls import path, include
from .views import GalleryListView, BulkUpload
app_name = 'medialogue'
urlpatterns = [
	path('', GalleryListView.as_view(), name='gallery-list'),
        path('upload/', BulkUpload, name='bulk-upload'),
        path('fp/', include('django_drf_filepond.urls')),
]
