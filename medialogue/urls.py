from django.urls import path, include, re_path, reverse_lazy
from .views import *
from django.views.generic import RedirectView

app_name = 'medialogue'
urlpatterns = [
        path('',
            RedirectView.as_view(
                url=reverse_lazy('medialogue:ml-album-list'), 
                permanent=True
            ),
            name='ml-medialogue-root'
        ),
	path('api/', include('medialogue.api.urls')),
	path('albums/', AlbumListView.as_view(), name='ml-album-list'),
        path('album/new/', NewAlbum, name='new-album'),
        re_path('album/(?P<slug>[\-\d\w]+)/edit/$', AlbumEditView, name='ml-album-edit'),
        re_path('album/(?P<slug>[\-\d\w]+)/$', AlbumDetailView.as_view(), name='ml-album'),
        re_path('video/(?P<slug>[\-\d\w]+)/$', VideoDetailView.as_view(), name='ml-video'),
        path('photos/', PhotoListView.as_view(), name='ml-photo-list'),
        path('videos/', VideoListView.as_view(), name='ml-video-list'),
        re_path('^photo/(?P<slug>[\-\d\w]+)/$', PhotoDetailView.as_view(), name='ml-photo'),
        path('fp/', include('django_drf_filepond.urls')),
]
