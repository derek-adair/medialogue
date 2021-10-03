docker-compose run --rm web django-admin startproject $1 . \
    && docker-compose run --rm web python ./manage.py migrate \
    && sudo chown -R $(whoami):$(whoami) . \
    && rm -rf .git \
    && git init \
    && git add . \
    && git commit -m "Bootstrapped $1"
