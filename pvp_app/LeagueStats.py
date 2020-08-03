from pvp_app.models import BaseStats

# Class definition of dictionary that will store 4096 PVP stat product calculations and ranks

class LeagueStats:
    def __init__(self, pokemon, league):
        self.pokemon = pokemon
        self.league = league
        self.league_dic = {}

    def calculate_4096_stat_products(self):
        # find base stats for pokemon (case-insensitive exact match)
        base_stats = BaseStats.objects.get(species__iexact=self.pokemon)
        print(base_stats.display_base_stats())


        return self.league_dic