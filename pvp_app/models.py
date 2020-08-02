from django.db import models

# Create your models here.

class BaseStats(models.Model):
    p_id = models.CharField(max_length=25)
    species = models.CharField(max_length=100)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()


    def __str__(self):
        return self.species