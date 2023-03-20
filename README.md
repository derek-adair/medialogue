# Medialogue

Medialogue is a fork of of [photologue](https://github.com/richardbarran/django-photologue) with video support and a more modern feel.

## Quick Start
**Clone & start the container**
```
git clone https://github.com/derek-adair/medialogue && \
cd medialogue && cp .example.env-dev .env-dev && \
docker-compose up
# Now you will see medialogue_web_1 / medialogue_redis_1 started
``
**attach to the container & activate virtualenv**
``
docker exec -it medialogue_web_1
# You should now see root@5de3137f66df:/code#
. /virtualenv/bin/activate

# You should now see (virtualenv) root@5de3137f66df:/code#
```
**Apply migrations**
```
./manage.py migrate
```

**Start django RQ**
```
./manage.py rqworker default
```

Now Medialogue is running on localhost:8001 with a djangorq worker started, pointing to our redis container.  If you followed these directions you should see the django-rq worker console output.  In another terminal you can easily attach to the web console output by running `docker attach medialogue_web_1`.

### Major Changes From Photologue
**Video Support**: Using [django video encoding](https://github.com/escaped/django-video-encoding)
**Front end focus**: I've completely disregarded the admin UI for the end user.  Here are a couple neat features;
1. Smooth upload experience.
2. Edit/upload/order media outside of admin UI
3. Thumbnails with easy_thumbnails

### Breaking Changes
1. Changed Gallery -> Album
2. I've removed the manyToMany relationship between media/albums.  I am now using [django-ordered-model](https://github.com/django-ordered-model/django-ordered-model) and a one to many relationship.

*I have no interest/bandwidth to develop a migration from photologue->medialogue; but would welcome a PR*
