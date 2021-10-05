from django.urls import path
from .views import GalleryListView
app_name = 'medialogue'
urlpatterns = [
	path('',
        GalleryListView.as_view(),
        name='gallery-list'),
]
