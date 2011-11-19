To set up django app:

    $ cd /tapkick/web
    $ virtualenv env
    $ ln -s /en/bin/activate
    $ source activate
    $ pip install -r requirements.txt
    $ cd webapp
    $ ln -s ../../design static
    $ cd templates
    $ ln -s ../../env/lib/python2.7/site-packages/django/contrib/admin/templates/admin
    $ cd ../
    $ python manage.py syncdb
    $ python manage.py runserver 0.0.0.0:8080

Then browse to the application.


