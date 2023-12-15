#!/usr/bin/env sh


NAME="to_do_list_api"
DJANGO_WSGI_MODULE=to_do_list_api.wsgi
NUM_WORKERS=3

if ! python manage.py test --k; then
    echo '[ ALERT: Application not pass in the tests. ]'
    exit 1
else
    echo '[ INFO: Success in all tests of the Application. ]'
fi

python manage.py makemigrations
python manage.py migrate

gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name ${NAME} \
    --timeout 120 \
    --workers ${NUM_WORKERS} \
    --threads 2 \
    --bind 0.0.0.0:8000 \
    --log-config gunicorn.conf \
    --log-syslog-prefix gunicorn \
    --log-level=info