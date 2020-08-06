# Generated by Django 3.0.8 on 2020-08-06 23:11

from django.db import migrations, models
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_id', models.CharField(max_length=25)),
                ('species', models.CharField(max_length=100)),
                ('hp', models.IntegerField()),
                ('attack', models.IntegerField()),
                ('defense', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CPMultipliers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.FloatField()),
                ('cp_multiplier', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='LevelPowerUpCosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.FloatField()),
                ('stardust', models.IntegerField()),
                ('candy', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PokemonPVP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('species', models.CharField(max_length=100)),
                ('GL_dic', picklefield.fields.PickledObjectField(editable=False)),
                ('UL_dic', picklefield.fields.PickledObjectField(editable=False)),
                ('ML_dic', picklefield.fields.PickledObjectField(editable=False)),
            ],
        ),
    ]
