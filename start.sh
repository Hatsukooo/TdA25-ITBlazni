#!/bin/sh
python3 manage.py makemigrations
# Apply database migrations
python3 manage.py migrate

# Start the server
python3 manage.py runserver 0.0.0.0:8000