@echo off
title ITBlazni
py -3 manage.py makemigrations

py -3 manage.py migrate

py -3 manage.py runserver 0.0.0.0:8000