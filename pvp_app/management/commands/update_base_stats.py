from django.core.management.base import BaseCommand
from django.db import connection
from pvp_app.models import BaseStats
from fullstack_pvp_project.settings import BASE_DIR
import os
import csv

def old_copy_from_csv():
    # TODO: come up with way that can write base stats to database without needing special permissions
    # in heroku db CLI, open psql and use:
    # "\COPY pvp_app_basestats (p_id, species, hp, attack, defense) FROM 'pvp_app/pogostats_csv.csv' (format csv, header true);"
    # copies base stat data from CSV file to Postgresql table
    with connection.cursor() as cursor:
        cursor.execute("COPY pvp_app_basestats (p_id, species, hp, attack, defense) FROM %s (format csv, header true);", [os.path.join(BASE_DIR, 'pvp_app/pogostats_csv.csv')])
        return


def copy_from_csv():
    i = 0

    with open(os.path.join(BASE_DIR, "pvp_app/pogostats_csv.csv"), newline='', encoding='utf-8-sig') as base_file:
        read_file = csv.reader(base_file)
        for row in read_file:
            # skip header line
            print(row)
            if i == 0: 
                i += 1
                continue
            BaseStats.objects.create(p_id=row[0], species=row[1], hp=row[2], attack=row[3], defense=row[4])



def delete_old_entries():
    # deletes entries from base stat table
    BaseStats.objects.all().delete()
    

class Command(BaseCommand):
    help: "Updates database table of Pokemon base stats"

    def handle(self, *args, **options):
        delete_old_entries()
        copy_from_csv()
        self.stdout.write('Base Stats updated')