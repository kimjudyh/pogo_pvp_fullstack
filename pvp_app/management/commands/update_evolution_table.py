from django.core.management.base import BaseCommand
from django.db import connection
from pvp_app.models import EvolutionTable
from fullstack_pvp_project.settings import BASE_DIR
import os

def copy_from_csv():
    import csv
    first_evo = []
    second_evo = []
    third_evo = []

    with open(os.path.join(BASE_DIR, "pvp_app/pokemon_evolutions.csv"), newline='', encoding='utf-8-sig') as evo_file:
        read_file = csv.reader(evo_file)
        for row in read_file:
            # check if first cell is empty or contains a pokemon
            # if empty, keep previous arrays bc it is a multi-path evolution chain
            # ex. ralts, kirlia, gardevoir OR gallade
            if row[0] != '' or row[0] == 'end':
                # write arrays to database
                if first_evo != []:
                    EvolutionTable.objects.create(species=first_evo[0], evolution=first_evo)
                if second_evo != []:
                    EvolutionTable.objects.create(species=second_evo[0], evolution=second_evo)
                if third_evo != []:
                    EvolutionTable.objects.create(species=third_evo[0], evolution=third_evo)
                # create empty array
                first_evo = []
                second_evo = []
                third_evo = []

            print(row)
            i = 0
            for cell in row:
                if i == 0 and cell != '':
                    # first cell of row contains pokemon like bulbasaur
                    first_evo.append(cell)
                elif i == 1 and cell != '' and row[0] != '':
                    # second cell of row contains pokemon like ivysaur
                    # and first cell of row is not empty
                    # append to first evo's array
                    first_evo.append(cell)
                    # append to second evo's array
                    second_evo.append(cell)
                elif i == 1 and cell != '' and row[0] == '':
                    # first cell empty, second cell is not
                    # add second cell contents to first evo's array
                    first_evo.append(cell)
                    # write to database
                    EvolutionTable.objects.create(species=second_evo[0], evolution=second_evo)
                    # clear out second evo's array and append
                    second_evo = []
                    second_evo.append(cell)
                elif i == 2 and cell != '' and row[0] != '' and row[1] != '':
                    # third cell of row contains pokemon like venusaur
                    # and first, second cells are not empty
                    # append to first evo's array
                    first_evo.append(cell)
                    # append to second evo's array
                    second_evo.append(cell)
                    # append to third evo's array
                    third_evo.append(cell)
                elif i == 2 and cell != '' and row[0] == '' and row[1] == '':
                    # first and second cells empty, third is not
                    # add third cell contents to first, second evo's arrays
                    first_evo.append(cell)
                    second_evo.append(cell)
                    # write to database
                    EvolutionTable.objects.create(species=third_evo[0], evolution=third_evo)
                    # clear out third evo's array and append
                    third_evo = []
                    third_evo.append(cell)

                i += 1
            # at the end of the row, write arrays to database
            print('first_evo', first_evo)
            # EvolutionTable.objects.create(species=first_evo[0], evolution=first_evo)
            # if second and third evo arrays exist, write them to database
            if second_evo != []:
                print('second evo', second_evo)
            if third_evo != []:
                print('third evo', third_evo)


def delete_old_entries():
    # deletes entries from evolution table
    EvolutionTable.objects.all().delete()

class Command(BaseCommand):
    help: "Updates database table of Pokemon base stats"

    def handle(self, *args, **options):
        delete_old_entries()
        copy_from_csv()
        self.stdout.write('Evolution Table updated')