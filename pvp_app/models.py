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


class PokemonPVP(models.Model):
    species = models.CharField(max_length=100)
    # League_dic definition
    # { IV combo as a string: { rank: int, stat_product: float } }
    # { '000': { 'rank': 123, 'stat_product': 123.33 }}
    GL_dic = PickledObjectField()
    UL_dic = PickledObjectField()
    ML_dic = PickledObjectField()

    def __str__(self):
        return ('PVP stats')
