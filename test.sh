if ! python manage.py test --k; then
    echo '[ ALERT: Application not pass in the tests. ]'
    exit 1
else
    echo '[ INFO: Success in all tests of the Application. ]'
fi