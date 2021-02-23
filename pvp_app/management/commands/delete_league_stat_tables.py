from django.core.management.base import BaseCommand
from django.db import connection
from pvp_app.models import PokemonPVP
from fullstack_pvp_project.settings import BASE_DIR
import os

def delete_old_entries():
    # deletes entries from League stats table
    PokemonPVP.objects.all().delete()
    

class Command(BaseCommand):
    help: "Deletes database tables of Pokemon stat products"

    def handle(self, *args, **options):
        delete_old_entries()
        self.stdout.write('Stat product tables deleted')