from pvp_app.models import BaseStats, CPMultipliers, PokemonPVP
from fullstack_pvp_project.settings import BASE_DIR
import math as m
import os

# Class definition of dictionary that will store 4096 PVP stat product calculations and ranks

class LeagueStats:
    def __init__(self, pokemon):
        self.pokemon = pokemon
        self.league_dic = {}
        self.stat_product_array = []
        self.IV_combo_dic = {}


    def verify_evo_pokemon(self):
        base_stats = BaseStats.objects.filter(species__iexact=self.pokemon)
        if not base_stats:
            return False
        else:
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

        return dic_cp_mult


    def calculate_4096_stat_products(self, league, max_level):
        # get table from database for this pokemon, or create it if it doesn't exist
        PVP_table, created = PokemonPVP.objects.get_or_create(species__iexact=self.pokemon.lower(), 
        defaults=
        { 'species': self.pokemon.lower(), 'GL_dic': {}, 'UL_dic': {}, 'ML_dic': {}
        })
        # print(PVP_table.species)
        

        # find base stats for pokemon (case-insensitive exact match)
        base_stats = BaseStats.objects.get(species__iexact=self.pokemon)
        # account for misspelled pokemon
        # print(base_stats.display_base_stats())

        stam_base = base_stats.hp
        atk_base = base_stats.attack
        def_base = base_stats.defense

        # get all cp multipliers and levels
        # cp_multipliers = CPMultipliers.objects.all()
        dic_cp_mult = self.read_cp_mult()

        stam_IV = list(range(0, 16))
        atk_IV = list(range(0, 16))
        def_IV = list(range(0, 16))

        if league == "GL":
            max_cp = 1500
        elif league == "UL":
            max_cp = 2500
        elif league == "ML":
            max_cp = 9000
        else:
            print(f"League name {league} is invalid")
            return

        # Start at level 1.
        min_level = 1
        # min_cpm = cp_multipliers.get(level=min_level).cp_multiplier
        min_cpm = dic_cp_mult[min_level]
        # print(min_cpm)


        # stat_product = []
        for i_stam in stam_IV:
            for j_atk in atk_IV:
                for k_def in def_IV:
                    S = stam_base + i_stam
                    A = atk_base + j_atk
                    D = def_base + k_def

                    cp = max(10, m.floor(.1*A*m.sqrt(D*S)*min_cpm**2))
                    if cp <= max_cp:
                        level = min_level
                        while cp <= max_cp and level < max_level:
                            level += .5
                            cp_mult = dic_cp_mult[level]
                            cp = max(10, m.floor(.1*A*m.sqrt(D*S)*cp_mult**2))
                        if cp > max_cp: # we exit the previous loop when the max cp is exceeded
                            level -= .5
                        cp_mult = dic_cp_mult[level]
                        cp = m.floor(.1*A*m.sqrt(D*S)*cp_mult**2)

                        product = m.floor(S*cp_mult)*A*D*cp_mult**2

                        # write to array of stat products
                        self.stat_product_array.append(product)

                        # write to IV combo dic A/D/S
                        IV_combo = str(j_atk) + ',' + str(k_def) + ',' + str(i_stam) 
                        # in case of duplicate stat products for different IV combos
                        if product not in self.IV_combo_dic:
                            self.IV_combo_dic[product] = [IV_combo]
                        else:
                            self.IV_combo_dic[product].append(IV_combo)

                        # write to league_dic
                        self.league_dic[IV_combo] = {
                            'rank': 0,
                            'stat_product': product,
                            'percent_of_max': 0.0
                        }

        max_product = max(self.stat_product_array)
        min_product = min(self.stat_product_array)
        print('max product', max_product)
        print('min product', min_product)

        # sort array in descending order
        self.stat_product_array.sort(reverse=True)

        # write rank to league_dic
        rank = 1
        for product in self.stat_product_array:
            IV_combo_list = self.IV_combo_dic[product]
            for IV_combo in IV_combo_list:
                self.league_dic[IV_combo]['rank'] = rank
                self.league_dic[IV_combo]['percent_of_max'] = product/max_product * 100
            rank += 1

        # write to database
        if league == "GL":
            PVP_table.GL_dic = self.league_dic
        elif league == "UL":
            PVP_table.UL_dic = self.league_dic
        elif league == "ML":
            PVP_table.ML_dic = self.league_dic

        PVP_table.save()

        # reset arrays and dics to be empty
        self.league_dic = {}
        self.stat_product_array = []
        self.IV_combo_dic = {}

        return 

    def get_stat_product(self, league, attack, defense, stamina, max_level):
        # get table from database for this pokemon, or create it if it doesn't exist
        '''
        PVP_table, created = PokemonPVP.objects.get_or_create(species__iexact=self.pokemon.lower(), 
        defaults=
        { 'species': self.pokemon.lower(), 'GL_dic': {}, 'UL_dic': {}, 'ML_dic': {}
        })
        '''

        # check if database has calculated dictionary of stat products
        #if created or not PVP_table.stats_have_been_calculated(league):
        self.calculate_4096_stat_products(league, max_level)
        # refetch from database
        PVP_table = PokemonPVP.objects.get(species__iexact=self.pokemon.lower())

        IV_combo = str(attack) + ',' + str(defense) + ',' + str(stamina)
        
        if league == 'GL':
            # print(PVP_table.GL_dic[IV_combo])
            return PVP_table.GL_dic[IV_combo]
        elif league == 'UL':
            # print(PVP_table.UL_dic[IV_combo])
            return PVP_table.UL_dic[IV_combo]
        elif league == 'ML':
            # print(PVP_table.ML_dic[IV_combo])
            return PVP_table.ML_dic[IV_combo]
        



        return 
