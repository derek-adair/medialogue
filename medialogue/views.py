from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from .forms import NewAlbumForm, EditAlbumForm
#@TODO - refactor MediaAlbum model name to Album
from .models import Album, Video, Photo
from .utils import querydict_to_dict

class AlbumListView(ListView):
    queryset = Album.objects.is_public().on_site()

class AlbumDetailView(DetailView):
    queryset = Album.objects.is_public().on_site()

@require_http_methods(['GET', 'POST'])
def AlbumEditView(request, slug):
    album = get_object_or_404(Album, slug=slug)
    form = EditAlbumForm(request.POST or None, instance=album)
    if request.POST:
        if form.is_valid():
            form.save()
    return render(request, 'medialogue/album_edit.html', {'form': form, 'album': album})

class PhotoListView(ListView):
    queryset = Photo.objects.on_site().is_public()
    paginate_by = 20

class VideoListView(ListView):
    queryset = Video.objects.on_site().is_public()
    paginate_by = 20

class PhotoDetailView(DetailView):
    queryset = Photo.objects.on_site().is_public()

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
