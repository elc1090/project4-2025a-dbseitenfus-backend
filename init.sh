#!/bin/bash
python manage.py migrate
python manage.py makemigrations
python manage.py collectstatic --noinput