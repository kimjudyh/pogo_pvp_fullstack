release: python2 manage.py migrate --fake pvp_app zero
release: python3 manage.py migrate pvp_app --fake-initial
web: gunicorn fullstack_pvp_project.wsgi --log-file -
