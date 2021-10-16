from django.urls import path, include, re_path
from .views import GalleryListView, BulkUpload, VideoDetailView
app_name = 'medialogue'
urlpatterns = [
	path('', GalleryListView.as_view(), name='gallery-list'),
        path('upload/', BulkUpload, name='bulk-upload'),
        re_path('video/(?P<slug>[\-\d\w]+)/$', VideoDetailView.as_view(), name='ml-video'),
        path('fp/', include('django_drf_filepond.urls')),
]
