@echo off

REM 1) Activate the virtual environment
call venv\Scripts\activate.bat

REM 2) Set Flask app to your factory function in app\app.py
set FLASK_APP=app.app:create_app

REM 3) Optional: enable debug mode
set FLASK_ENV=development

REM 4) Run Flask
python -m flask run

REM 5) Pause so the window stays open
pause
