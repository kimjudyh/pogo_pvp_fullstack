from django.db import models
from picklefield.fields import PickledObjectField

# Create your models here.

class BaseStats(models.Model):
    p_id = models.CharField(max_length=25)
    species = models.CharField(max_length=100)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()


    def __str__(self):
        return self.species
    
    def display_base_stats(self):
        return f"attack: {self.attack}, defense: {self.defense}, stamina: {self.hp}"


class CPMultipliers(models.Model):
    level = models.FloatField()
    cp_multiplier = models.FloatField()

    def __str__(self):
        return('Level CP Multipliers')


class LevelPowerUpCosts(models.Model):
    level = models.FloatField()
    stardust = models.IntegerField()
    candy = models.IntegerField()

    def __str__(self):
        return('Level Power Up Costs')


class PokemonPVP(models.Model):
    species = models.CharField(max_length=100)
    # League_dic definition
    # { IV combo as a string: { rank: int, stat_product: float } }
    # { '0,0,0': { 'rank': 123, 'stat_product': 123.33 }}
    GL_dic = PickledObjectField()
    UL_dic = PickledObjectField()
    ML_dic = PickledObjectField()

    def __str__(self):
        return (f'PVP stats for {self.species}')

    def stats_have_been_calculated(self, league):
        # return true if league stats have been calculated
        # return false if dictionary is empty

        if league == 'GL':
            return bool(self.GL_dic)
        elif league == 'UL':
            return bool(self.UL_dic)
        elif league == 'ML':
            return bool(self.ML_dic)
        else:
            return


class EvolutionTable(models.Model):
    species = models.CharField(max_length=100)
    evolution = PickledObjectField()

    def __str__(self):
        return 'evolution table'


    
