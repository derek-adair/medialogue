# Medialogue
The purpose of medialogue is to handle multimedia uploads from users in an extensible and customizable fashion.  

## Install
Registered as `django-medialogue` on [pypi](https://pypi.org/project/django-medialogue/)
```
pip install django-medialogue
```

Configure;
```
#settings.py
INSTALLED_APPS=[
    'medialogue'
    #...
]
#urls.py
urlpatterns = [
    # ...
    path('', include('medialogue.urls', namespace='medialogue')),

# Make sure you are serving the user media
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

*There is probably more stuff to do; this is all a WIP and no one uses this yet anyways ;)*

## Run tests
```
# start up the test container
$> docker compose run --rm web bash -il
# Activate Virtual Env
$docker-container> . /virtualenv/bin/activate
# Start the test loop (uses [pytest](https://docs.pytest.org/en/7.2.x/) / [pytest-django](https://pytest-django.readthedocs.io/en/latest/)
$docker-container> ./testrunner.sh
```
