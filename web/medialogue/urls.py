from .views import GalleryListView
app_name = 'photologue'
urlpatterns = [
	path('',
        GalleryListView.as_view(),
        name='gallery-list'),
]
