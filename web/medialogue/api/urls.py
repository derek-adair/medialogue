from django.urls import path, include
from .views import reorder_media, add_to_album
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('reorder-media/<int:pk>/', reorder_media, name='reorder-media'),
    path('add-to-album/<int:pk>/', add_to_album, name='add-to-album'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
