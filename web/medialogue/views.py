from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from .forms import NewAlbumForm
#@TODO - refactor MediaAlbum model name to Album
from .models import Album, Video, Photo

class AlbumListView(ListView):
    queryset = Album.objects.is_public().on_site()

class AlbumDetailView(DetailView):
    queryset = Album.objects.is_public().on_site()

class PhotoListView(ListView):
    queryset = Photo.objects.on_site().is_public()
    paginate_by = 20

class VideoListView(ListView):
    queryset = Video.objects.on_site().is_public()
    paginate_by = 20

class PhotoDetailView(DetailView):
    queryset = Photo.objects.on_site().is_public()

def querydict_to_dict(query_dict):
    # request.POST only returns the first value in a list, this grabs it all
    # Lovingly stolen from: https://tinyurl.com/h6my82s6
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
    return data

@require_http_methods(['GET', 'POST'])
def NewAlbum(request):
    if request.method == 'POST':
        post_data = querydict_to_dict(request.POST)
	# Remove the blank value associated with the automatic rendering of BulkMediaForm
	# @TODO - option 1) modify filepond to add id's as a vlue in csv
	#         option 2) manually render the form and exclude filepond input
        if '' in post_data['filepond']:
            post_data['filepond'].remove('')
        form = NewAlbumForm(post_data)
        if form.is_valid():
            slug = form.save()
            return HttpResponseRedirect(reverse('medialogue:ml-album', args=[slug]))
    else:
        form = NewAlbumForm()

    return TemplateResponse(request, 'medialogue/new-album.html', {'form': form})

class VideoDetailView(DetailView):
    queryset=Video.objects.on_site().is_public()
