FROM python:3.9-alpine3.13
LABEL mantainer="jonamk1"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /temp/requirements.txt
COPY ./requirements.dev.txt /temp/requirements.dev.txt

COPY /app /app
WORKDIR /app
EXPOSE 8000

ARG DEV="false"
RUN python -m venv /pyenvironment && \
    /pyenvironment/bin/pip install --upgrade pip && \
        apk add --update --no-cache postgresql-client && \
        apk add --update --no-cache --virtual .tmp-build-deps \
          build-base postgresql-dev musl-dev && \
    /pyenvironment/bin/pip install -r /temp/requirements.txt && \
    if [ $DEV = "true" ]; then \
     /pyenvironment/bin/pip install -r /temp/requirements.dev.txt ; \
    fi && \
    rm -rf /temp && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/pyenvironment/bin/:$PATH"

USER django-user