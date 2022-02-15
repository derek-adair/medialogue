from django.urls import path, include, re_path
from .views import *
app_name = 'medialogue'
urlpatterns = [
	path('album/', AlbumListView.as_view(), name='ml-album-list'),
        path('album/new/', NewAlbum, name='new-album'),
        re_path('video/(?P<slug>[\-\d\w]+)/$', VideoDetailView.as_view(), name='ml-video'),
        re_path('album/(?P<slug>[\-\d\w]+)/$', AlbumDetailView.as_view(), name='ml-album'),
        path('fp/', include('django_drf_filepond.urls')),
]
