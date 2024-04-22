web: python3 manage.py collectstatic --noinput && uwsgi --static-map /static=/workspace/app/static --ini uwsgi.ini

celery_worker: celery --app config.celery:app worker --loglevel info
celery_beat: celery --app config.celery:app beat --loglevel info --scheduler django

migrations: python3 manage.py migrate

tests: pytest
shell_plus: python3 manage.py shell_plus
dbshell: python3 manage.py dbshell
debug: python3 manage.py collectstatic --noinput && python3 manage.py runserver 0.0.0.0:$PORT
runserver_local: python3 manage.py runserver_plus 0.0.0.0:8000 --reloader-type stat
celery_debug: celery --app config.celery:app worker --beat --scheduler=django --loglevel=info
health_check: python3 manage.py health_check

freeze: sleep 3000
