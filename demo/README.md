# Quick Start
### Clone & start the container
```
git clone https://github.com/derek-adair/medialogue && \
cd medialogue && cp .example.env-dev .env-dev && \
docker-compose up -d
```
**Now you will see something like...**
```
Starting medialogue_redis_1 ... done
Creating medialogue_testrunner_1 ... done
Creating medialogue_demo_1       ... done
```


### attach to the container & activate virtualenv
```
docker exec -it medialogue_demo_1 bash -il
```
**You should now see something like...  root@5de3137f66df:/code#**

### Activate virtualenv
```
. /virtualenv/bin/activate
```
**You should now see (virtualenv) root@5de3137f66df:/code#**

### Apply migrations
```
./manage.py migrate
```

**Start django RQ**
```
./manage.py rqworker default
```

### App is Running!
You can navigate to localhost:8001 to observe how end users can add albums and view media.
