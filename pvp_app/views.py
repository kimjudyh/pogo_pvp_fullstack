from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .LeagueStats import LeagueStats
from .PowerUpStats import PowerUpStats

# Create your views here.

def home(request):
    template = 'home.html'
    return render(request, template)


def analyze(request):
    if request.method == 'POST':
        print(request.POST)

        # deal with multiple entries

        req_pokemon = request.POST['pokemon']
        evo_pokemon = request.POST['evo_pokemon']

        # get stat product for the requested evolution pokemon
        evo_pokemon_pvp = LeagueStats(evo_pokemon.lower())
        pokemon_power_up = PowerUpStats(req_pokemon.lower())
        results = []
        stats = {}
        inputs = {}
        # stats_array = []
        # power_up_array = []

        analyze_GL = False
        analyze_UL = False
        analyze_ML = False

        try:
            if request.POST['GL'] == 'true':
                analyze_GL = True
            if request.POST['UL'] == 'true':
                analyze_UL = True
            if request.POST['ML'] == 'true':
                analyze_ML = True
        except:
            pass


        # need to use getlist to save all values, otherwise will default to giving just last value
        c = request.POST.getlist('cp')
        a = request.POST.getlist('attack')
        d = request.POST.getlist('defense')
        s = request.POST.getlist('stamina')
        print(c, a, d, s)

        # multiple entries: 'attack': [1, 3, 6] etc.
        for cp, attack, defense, stamina in zip(c, a, d, s):
            if cp != '' and attack != '' and defense != '' and stamina != '':
                if analyze_GL:
                    stats_GL = evo_pokemon_pvp.get_stat_product('GL', int(attack), int(defense), int(stamina))
                    stats['GL'] = stats_GL
                if analyze_UL:
                    stats_UL = evo_pokemon_pvp.get_stat_product('UL', int(attack), int(defense), int(stamina))
                    stats['UL'] = stats_UL
                if analyze_ML:
                    stats_ML = evo_pokemon_pvp.get_stat_product('ML', int(attack), int(defense), int(stamina))
                    stats['ML'] = stats_ML

                inputs['attack'] = attack
                inputs['defense'] = defense
                inputs['stamina'] = stamina
                inputs['cp'] = cp
                # stats_array.append(stats)
                # print(stats_array)

                power_up = pokemon_power_up.calc_evolve_cp(evo_pokemon.lower(), int(cp), int(attack), int(defense), int(stamina))
                # power_up_array.append(power_up)
                # print(power_up_array)

                results.append({
                    'inputs': inputs,
                    'stats': stats,
                    'power_up': power_up
                })

                print(results)


        # attack = request.POST['attack']
        # defense = request.POST['defense']
        # stamina = request.POST['stamina']

        # stats = pokemon.get_stat_product('GL', attack, defense, stamina)

        template = 'home.html'
        context = {
            'pokemon': req_pokemon,
            'evolution': evo_pokemon,
            'analyze_GL': analyze_GL,
            'analyze_UL': analyze_UL,
            'analyze_ML': analyze_UL,
            # 'cp': request.POST['cp'],
            # 'attack': request.POST['attack'],
            # 'defense': request.POST['defense'],
            # 'stamina': request.POST['stamina'],
            # 'stats_array': stats_array,
            # 'power_up_array': power_up_array,
            'results': results
        }
        return render(request, template, context)
        # return JsonResponse(stats)


        # return HttpResponse('<h1>yo</h1>')


    

