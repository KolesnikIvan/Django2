rem file that starts server
call ..\venv\Scripts\activate.bat
call echo hello
call python manage.py runserver
call echo world
call cmd /k