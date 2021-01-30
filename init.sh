#!/bin/bash

rm -rf blog.db
rm -rf myblog/migrations
rm -rf photo/migrations
rm -rf spider/migrations
python manage.py makemigrations myblog
python manage.py makemigrations photo
python manage.py makemigrations spider
python manage.py migrate
python manage.py init_sys
python manage.py init_spider
python manage.py runserver