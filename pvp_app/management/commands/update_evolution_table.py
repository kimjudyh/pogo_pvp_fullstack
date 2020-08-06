from django.core.management.base import BaseCommand
from django.db import connection
from pvp_app.models import EvolutionTable
from fullstack_pvp_project.settings import BASE_DIR
import os

def copy_from_csv():
    import csv

    with open(os.path.join(BASE_DIR, "pvp_app/pokemon_evolutions.csv"), newline='') as evo_file:
        read_file = csv.reader(evo_file)
        for row in read_file:
            print(row)


def delete_old_entries():
    # deletes entries from evolution table
    EvolutionTable.objects.all().delete()

class Command(BaseCommand):
    help: "Updates database table of Pokemon base stats"

    def handle(self, *args, **options):
        delete_old_entries()
        copy_from_csv()
        self.stdout.write('Evolution Table updated')