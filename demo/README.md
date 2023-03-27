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
