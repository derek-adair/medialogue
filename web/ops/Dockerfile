FROM derekadair/python-workflow:dev as dev
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

FROM derekadair/python-workflow:ffmpeg

COPY --from=dev /virtualenv/ /virtualenv/
COPY --from=dev /usr/bin/entr /usr/bin/entr
COPY --from=dev /usr/bin/ag /usr/bin/ag

COPY ./ /code/
WORKDIR /code
