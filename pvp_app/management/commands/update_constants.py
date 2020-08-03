from django.core.management.base import BaseCommand
from django.db import connection
from pvp_app.models import CPMultipliers, LevelPowerUpCosts
from fullstack_pvp_project.settings import BASE_DIR
import os

# read and process cp multiplier data text file
def read_cp_mult():
    '''
    returns dictionary with key: level (float), value: cp multiplier (float)
    each level has a unique cp multiplier
    '''
    with open(os.path.join(BASE_DIR, "pvp_app/cp_mult_data.txt"), "r") as cp_mult_file:
        cp_mult_list = cp_mult_file.readlines()

    # remove header lines that label columns
    del(cp_mult_list[0:1])

    # initialize empty dictionary
    # dic_cp_mult = {}

    # remove \t and \n, place level and cp_mult pairs into dictionary
    for entry in cp_mult_list:
        x = entry.find("\t")
        y = entry.find("\n")
        if "\n" not in entry:
            # dic_cp_mult[float(entry[0:x])] = float(entry[x+1:])
            CPMultipliers.objects.create(
                level=float(entry[0:x]),
                cp_multiplier=float(entry[x + 1:]))
        else:
            CPMultipliers.objects.create(
                level=float(entry[0:x]),
                cp_multiplier=float(entry[x + 1: y]))
                # dic_cp_mult[float(entry[0:x])] = float(entry[x+1:y])

    # return dic_cp_mult
    return

def read_power_up_costs():
    '''
    returns dictionary with key: level (int), value: dictionary with keys:
    'stardust': int
    'candy': int
    ex. {10.5: {'stardust': 1000, 'candy': 1}}
    '''
    import csv

    dic_power_up = {}
    count = 0

    with open(os.path.join(BASE_DIR, "pvp_app/power_up_costs.csv"), newline='') as power_up_file:
        read_file = csv.reader(power_up_file)
        for row in read_file:
            # skip first line
            if count == 0:
                count += 1
                continue
            # dic_power_up[float(row[0])] = {'stardust': int(row[1]), 'candy': int(row[2])}
            LevelPowerUpCosts.objects.create(
                level=float(row[0]),
                stardust=int(row[1]),
                candy=int(row[2])
            )
    # return dic_power_up
    return


def delete_old_entries():
    CPMultipliers.objects.all().delete()
    LevelPowerUpCosts.objects.all().delete()
    return


class Command(BaseCommand):
    help: "Updates database tables of CP multipliers, stardust, candy, and level constants"

    def handle(self, *args, **options):
        # delete old entries
        delete_old_entries()
        self.stdout.write('deleted old entries')

        # write cp multiplier data
        read_cp_mult()
        self.stdout.write('updated cp multipliers')

        # write powerup cost data
        read_power_up_costs()
        self.stdout.write('updated power up costs')

        self.stdout.write('done')