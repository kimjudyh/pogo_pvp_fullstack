from django.core.management.base import BaseCommand
from django.db import connection
from pvp_app.models import BaseStats
from fullstack_pvp_project.settings import BASE_DIR
import os

def copy_from_csv():
    # copies base stat data from CSV file to Postgresql table
    with connection.cursor() as cursor:
        cursor.execute("COPY pvp_app_basestats (p_id, species, hp, attack, defense) FROM %s (format csv, header true);", [os.path.join(BASE_DIR, 'pvp_app/pogostats_csv.csv')])
        return

def delete_old_entries():
    # deletes entries from base stat table
    BaseStats.objects.all().delete()
    

class Command(BaseCommand):
    help: "Updates database table of Pokemon base stats"

    def handle(self, *args, **options):
        delete_old_entries()
        copy_from_csv()
        self.stdout.write('Base Stats updated')