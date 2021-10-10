from django.views.generic.list import ListView
from django.views.decorators.http import require_http_methods
from django.template.response import TemplateResponse
from .forms import BulkMediaForm
from .models import MediaGallery

class GalleryListView(ListView):
    queryset = MediaGallery.objects.is_public()

@require_http_methods(['GET', 'POST'])
def BulkUpload(request):
    if request.method == 'POST':
        form = BulkMediaForm(request.POST)
        if form.is_valid():
            pk = form.save()
            return HttpResponseRedirect('/galleries/{}'.format(pk))
    else:
        form = BulkMediaForm()

    return TemplateResponse(request, 'medialogue/bulk-upload.html', {'form': form})
