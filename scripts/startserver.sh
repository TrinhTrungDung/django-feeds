#!/bin/bash

# Build and start containers
docker-compose up -d --build

# Make neccessary database migrations
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate

# Force remove stopped containers
docker-compose rm -f