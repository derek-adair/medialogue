from medialogue.models import Media

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

@api_view(['POST'])
def reorder_media(request, pk):

    import pdb; pdb.set_trace()
