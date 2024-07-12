FROM python:3.13-rc-alpine3.19
LABEL mantainer="phionira.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /temp/requirements.txt
COPY ./requirements.dev.txt /temp/requirements.dev.txt

COPY /app /app
WORKDIR /app
EXPOSE 8000

ARG DEV="false"
RUN python -m venv /pyenvironment && \
    /pyenvironment/bin/pip install --upgrade pip && \
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