#!/bin/sh

set -e

celery -A src.config beat --loglevel=debug --pidfile= --scheduler django_celery_beat.schedulers:DatabaseScheduler
