#!/bin/sh


python manage.py makemigrations

python manage.py migrate --noinput



python manage.py collectstatic --noinput

# python manage.py createsuperuser --noinput
 daphne -b 0.0.0.0 -p 8000 backend.asgi:application
#daphne -u /tmp/daphne.sock backend.asgi:application

# for debug
#python manage.py runserver 0.0.0.0:8000