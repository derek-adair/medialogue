from django.core.exceptions import ObjectDoesNotExist
from medialogue.models import Media

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def reorder_media(request, pk):
    try:
        media = Media.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    order = request.POST.get('order', None)
    if order is None:
        return Response({"msg" : "order field required in form"}, status=status.HTTP_400_BAD_REQUEST)
    media.to(int(order))
    media.save()
    return Response({"msg":"{0} moved to {1}".format(media.title, request.data['order'])},
                    status=status.HTTP_200_OK)
