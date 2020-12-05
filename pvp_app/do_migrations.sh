#!/bin/bash
# give permission to run
# chmod +x script.sh
# run the script
# ./script.sh

# do stuff for migrations

# show migrations
python3 manage.py showmigrations
# fake reset migrations
python3 manage.py migrate --fake pvp_app zero
# remove all files from migrations folder except __init__.py
rm pvp_app/migrations/0*
rm -r pvp_app/migrations/__pycache__
# make migrations
python3 manage.py makemigrations
# fake initial migrations
python3 manage.py migrate --fake-initial
# show migrations
python3 manage.py showmigrations