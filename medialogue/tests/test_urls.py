from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

urlpatterns = [
    path('ptests/', include('medialogue.urls', namespace='medialogue')),
]
