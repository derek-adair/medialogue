## Django Development With Docker Compose
Start a django project in docker with *one* command
```
git clone git@github.com:derek-adair/docker-django-seed \
    && cd docker-django-seed \
    && ./bootstrap.sh PROJECT_NAME
```

You will end up in a folder `docker-django-seed` wherever you cloned this.  This folder will contain a django app that is ready to spin up...

```
docker-compose up
```

* Your app will be running on localhost:8000.
* You can rename docker-django-seed to whatever you want


## Usage
*create a django app*
```
comp run --rm web django-admin startapp YOUR_APP
```
All you need to do now is add `YOUR_APP` to `PROJECT_NAME.settings.py`
