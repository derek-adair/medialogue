from django.urls import path, include
from .views import reorder_media
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('reorder-media/<int:pk>/', reorder_media, name='reorder-media'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
