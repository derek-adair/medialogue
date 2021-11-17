from django.urls import path, include, re_path
from .views import MediaGalleryListView, MediaGalleryDetailView, BulkUpload, VideoDetailView
app_name = 'medialogue'
urlpatterns = [
	path('gallery/', MediaGalleryListView.as_view(), name='ml-gallery-list'),
        path('upload/', BulkUpload, name='bulk-upload'),
        re_path('video/(?P<slug>[\-\d\w]+)/$', VideoDetailView.as_view(), name='ml-video'),
        re_path('gallery/(?P<slug>[\-\d\w]+)/$', MediaGalleryDetailView.as_view(), name='ml-gallery'),
        path('fp/', include('django_drf_filepond.urls')),
]
