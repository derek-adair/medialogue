from django.conf import settings # import the settings file

def block_downloads(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'MEDIALOGUE_BLOCK_DOWNLOADS': settings.MEDIALOGUE_BLOCK_DOWNLOADS}
