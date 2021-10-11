from django.views.generic.list import ListView
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from .forms import BulkMediaForm
from .models import MediaGallery

class GalleryListView(ListView):
    queryset = MediaGallery.objects.is_public()

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
def BulkUpload(request):
    if request.method == 'POST':
        post_data = querydict_to_dict(request.POST)
	# Remove the blank value associated with the automatic rendering of BulkMediaForm
	# @TODO - option 1) modify filepond to add id's as a vlue in csv
	#         option 2) manually render the form and exclude filepond input
        post_data['filepond'].remove('')
        form = BulkMediaForm(post_data)
        if form.is_valid():
            pk = form.save()
            return HttpResponseRedirect('/galleries/{}'.format(pk))
    else:
        form = BulkMediaForm()

    return TemplateResponse(request, 'medialogue/bulk-upload.html', {'form': form})
