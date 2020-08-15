from pvp_app.models import BaseStats, CPMultipliers, PokemonPVP
from fullstack_pvp_project.settings import BASE_DIR
import math as m
import os

class PowerUpStats:
    def __init__(self, pokemon):
        self.pokemon = pokemon


    def verify_pokemon(self):
        # find base stats for pokemon (case-insensitive exact match)
        # base_stats = BaseStats.objects.get(species__iexact=self.pokemon)
        base_stats = BaseStats.objects.filter(species__iexact=self.pokemon)

        # TODO: account for misspelled pokemon
        # no results found
        if not base_stats:
            return False
        else:
            base_stats = base_stats.first()

        print(base_stats.display_base_stats())

        self.stam_base = base_stats.hp
        self.atk_base = base_stats.attack
        self.def_base = base_stats.defense

        self.read_cp_mult()
        self.read_power_up_costs()

        return True

    
    # read and process cp multiplier data text file
    def read_cp_mult(self):
        '''
        returns dictionary with key: level (float), value: cp multiplier (float)
        each level has a unique cp multiplier
        '''
        with open(os.path.join(BASE_DIR, "pvp_app/cp_mult_data.txt"), "r") as cp_mult_file:
            cp_mult_list = cp_mult_file.readlines()

        # remove header lines that label columns
        del(cp_mult_list[0:1])

        # initialize empty dictionary
        dic_cp_mult = {}

        # remove \t and \n, place level and cp_mult pairs into dictionary
        for entry in cp_mult_list:
            x = entry.find("\t")
            y = entry.find("\n")
            if "\n" not in entry:
                dic_cp_mult[float(entry[0:x])] = float(entry[x+1:])
            else:
                dic_cp_mult[float(entry[0:x])] = float(entry[x+1:y])

        self.dic_cp_mult = dic_cp_mult

        return dic_cp_mult


    def read_power_up_costs(self):
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
                dic_power_up[float(row[0])] = {'stardust': int(row[1]), 'candy': int(row[2])}

        self.dic_power_up = dic_power_up

        return dic_power_up

    
    def verify_IV_inputs(self, cp, atk_IV, def_IV, stam_IV):

        for level, i_cpm in self.dic_cp_mult.items():
            # calculate cp
            calc_cp = m.floor(.1*(self.atk_base + atk_IV)*\
                    m.sqrt(self.def_base + def_IV)*\
                    m.sqrt(self.stam_base + stam_IV)*i_cpm**2)
            if cp == calc_cp:
                self.starting_cp_mult = i_cpm
                self.starting_level = level
                return True

        print('error: wrong IVs')
        return False

    def calc_evolve_cp(self, evo_pokemon, cp, atk_IV, def_IV, stam_IV):
        '''
        :param evo_pokemon: string of evolution pokemon
        '''

        # self.verify_IV_inputs(cp, atk_IV, def_IV, stam_IV)

        # initialize vars for stardust and candy cost
        stardust_cost = 0
        candy_cost = 0

        # initialize var for number of power ups
        power_up_count = 0

        # find base stats of evolution pokemon
        # find base stats for pokemon (case-insensitive exact match)
        base_stats = BaseStats.objects.get(species__iexact=evo_pokemon)
        stam_base = base_stats.hp
        atk_base = base_stats.attack
        def_base = base_stats.defense

        # calculate CP, rounding down
        calc_cp = m.floor(.1*(atk_base + atk_IV)*\
                m.sqrt(def_base + def_IV)*\
                m.sqrt(stam_base + stam_IV)*self.starting_cp_mult**2)
        # calculate hp, rounding down
        calc_hp = m.floor(self.starting_cp_mult*(stam_base + stam_IV))


        # calculate closest cp to 1500
        cp_1500 = calc_cp
        #print("cp 1500", cp_1500)
        hp_1500 = calc_hp 
        cp_mult_1500 = self.starting_cp_mult
        level_1500 = self.starting_level

        # check if calc_cp is already over 1500
        if cp_1500 <= 1500:
            while cp_1500 <= 1500 and level_1500 < 40.0:
                # use level to get how much stardust, candy to power up
                stardust_cost += self.dic_power_up[level_1500]['stardust']
                candy_cost += self.dic_power_up[level_1500]['candy']

                # add to power up count, add 0.5 level
                power_up_count += 1
                level_1500 += 0.5
                
                # get new cp multiplier
                cp_mult_1500 = self.dic_cp_mult[level_1500]
                #print("cp_mult", cp_mult_1500)

                # calculate CP, rounding down
                cp_1500 = m.floor(.1*(atk_base + atk_IV)*\
                        m.sqrt(def_base + def_IV)*\
                        m.sqrt(stam_base + stam_IV)*cp_mult_1500**2)

                # calculate hp, rounding down
                hp_1500 = m.floor(cp_mult_1500*(stam_base + stam_IV))
            # since while loop will give cp over 1500, need to get the level below
            # and recalculate cp and hp
            if level_1500 == 40.0:
                pass
            else:
                power_up_count -= 1
                level_1500 -= 0.5
                stardust_cost -= self.dic_power_up[level_1500]['stardust']
                candy_cost -= self.dic_power_up[level_1500]['candy']

            cp_mult_1500 = self.dic_cp_mult[level_1500]
            # calculate CP, rounding down
            cp_1500 = m.floor(.1*(atk_base + atk_IV)*\
                    m.sqrt(def_base + def_IV)*\
                    m.sqrt(stam_base + stam_IV)*cp_mult_1500**2)
            # calculate hp, rounding down
            hp_1500 = m.floor(cp_mult_1500*(stam_base + stam_IV))

        # calculate closest CP to 2500 for Ultra League
        # start where Cp 1500 calcs left off
        cp_2500 = cp_1500
        cp_mult_2500 = cp_mult_1500
        level_2500 = level_1500
        stardust_2500 = stardust_cost
        candy_2500 = candy_cost
        power_up_2500 = power_up_count

        if level_2500 == 40.0:
            pass
        elif cp_2500 <= 2500:
            while cp_2500 <= 2500 and level_2500 < 40.0:
                stardust_2500 += self.dic_power_up[level_2500]['stardust']
                candy_2500 += self.dic_power_up[level_2500]['candy']
                power_up_2500 += 1
                level_2500 += 0.5
                cp_mult_2500 = self.dic_cp_mult[level_2500]
                cp_2500 = m.floor(.1*(atk_base + atk_IV)*\
                        m.sqrt(def_base + def_IV)*\
                        m.sqrt(stam_base + stam_IV)*cp_mult_2500**2)
            if level_2500 == 40.0:
                pass
            else:
                power_up_2500 -= 1
                level_2500 -= 0.5
                stardust_2500 -= self.dic_power_up[level_2500]['stardust']
                candy_2500 -= self.dic_power_up[level_2500]['candy']

            # calculate final values
            cp_mult_2500 = self.dic_cp_mult[level_2500]
            cp_2500 = m.floor(.1*(atk_base + atk_IV)*\
                    m.sqrt(def_base + def_IV)*\
                    m.sqrt(stam_base + stam_IV)*cp_mult_2500**2)

        # calculate max CP for Master League
        # start where cp 2500 calcs left off
        cp_max = cp_2500
        cp_mult_max = cp_mult_2500
        level_max = level_2500
        stardust_max = stardust_2500
        candy_max = candy_2500
        power_up_max = power_up_2500

        if level_max == 40.0:
            pass
        else:
            # calculate CP at level 40
            cp_mult_max = self.dic_cp_mult[40.0]
            cp_max = m.floor(.1*(atk_base + atk_IV)*\
                        m.sqrt(def_base + def_IV)*\
                        m.sqrt(stam_base + stam_IV)*cp_mult_max**2)
            while level_max < 40.0:
                stardust_max += self.dic_power_up[level_max]['stardust']
                candy_max += self.dic_power_up[level_max]['candy']
                power_up_max += 1
                level_max += 0.5

        power_up_dic = {}
        power_up_dic['GL'] = {
            'starting_cp': calc_cp, 
            'hp': calc_hp, 
            'starting_level': self.starting_level,
            'power_up_count': power_up_count, 
            'cp_1500': cp_1500, 
            'stardust_cost': stardust_cost, 
            'candy_cost': candy_cost, 
            'level_1500': level_1500
            }
        power_up_dic['UL'] = {
            'cp_2500': cp_2500, 
            'power_up_count': power_up_2500, 
            'stardust_cost': stardust_2500, 
            'candy_cost': candy_2500, 
            'level_2500': level_2500
            }
        power_up_dic['ML'] = {
            'cp_max': cp_max, 
            'power_up_count': power_up_max, 
            'stardust_cost': stardust_max, 
            'candy_cost': candy_max,
            'level_max': level_max
            }


        return power_up_dic