FROM derekadair/python-workflow:dev as dev
ENV PYTHONUNBUFFERED=1
WORKDIR /medialogue
COPY . /medialogue/
RUN pip install -r ./demo/requirements.txt

FROM derekadair/python-workflow:ffmpeg

COPY --from=dev /virtualenv/ /virtualenv/
COPY --from=dev /usr/bin/entr /usr/bin/entr
COPY --from=dev /usr/bin/ag /usr/bin/ag

COPY ./demo /code/
WORKDIR /code
