@ECHO OFF
ECHO ==================== Running stuff now ====================
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
ECHO ==================== DONE ====================
PAUSE