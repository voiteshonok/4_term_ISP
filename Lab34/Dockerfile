FROM python:3.8.3-alpine
WORKDIR /code

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt
COPY /app/ /code/

ENTRYPOINT ["/code/app/blogengine/entry.sh"]