from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .LeagueStats import LeagueStats
from .PowerUpStats import PowerUpStats
from .models import BaseStats, EvolutionTable

# Create your views here.

def home(request):
    template = 'home.html'
    return render(request, template)


def analyze(request):
    if request.method == 'GET':
        return redirect('home')
    elif request.method == 'POST':
        template = 'home.html'

        # deal with multiple entries

        req_pokemon = request.POST['pokemon']
        evo_pokemon = request.POST['evo-pokemon']

        # get stat product for the requested evolution pokemon
        evo_pokemon_pvp = LeagueStats(evo_pokemon.lower())
        pokemon_power_up = PowerUpStats(req_pokemon.lower())

        # check for valid Pokemon input
        species_is_valid = pokemon_power_up.verify_pokemon()
        if not species_is_valid:
            context = {
                'pokemon': req_pokemon,
                'evolution': evo_pokemon,
                'error': f'Invalid Pokemon: {req_pokemon}'
            }
            return render(request, template, context)
        
        # check for valid evolution Pokemon input
        evo_species_is_valid = evo_pokemon_pvp.verify_evo_pokemon()
        if not evo_species_is_valid:
            context = {
                'pokemon': req_pokemon,
                'evolution': evo_pokemon,
                'error': f'Invalid Evolution: {evo_pokemon}'
            }
            return render(request, template, context)

        results = []
        # stats_array = []
        # power_up_array = []

        analyze_GL = False
        analyze_UL = False
        analyze_ML = False

        try:
            if request.POST['GL'] == 'true':
                analyze_GL = True
        except:
            pass
        try:
            if request.POST['UL'] == 'true':
                analyze_UL = True
        except:
            pass
        try:
            if request.POST['ML'] == 'true':
                analyze_ML = True
        except:
            pass

        # print(analyze_GL, analyze_UL, analyze_ML)


        # need to use getlist to save all values, otherwise will default to giving just last value
        c = request.POST.getlist('cp')
        a = request.POST.getlist('attack')
        d = request.POST.getlist('defense')
        s = request.POST.getlist('stamina')
        # print(c, a, d, s)

        # multiple entries: 'attack': [1, 3, 6] etc.
        for cp, attack, defense, stamina in zip(c, a, d, s):
            stats = {}
            inputs = {}

            if cp != '' and attack != '' and defense != '' and stamina != '':
                # save inputs so they can be used in template to fill out form
                inputs['attack'] = attack
                inputs['defense'] = defense
                inputs['stamina'] = stamina
                inputs['cp'] = cp

                # verify IVs and CP
                is_valid = pokemon_power_up.verify_IV_inputs(int(cp), int(attack), int(defense), int(stamina))

                inputs['is_valid'] = is_valid

                if not is_valid:
                    # mark this entry as wrong to display on html
                    # print('invalid')
                    power_up = {}
                else:
                    # proceed

                    if analyze_GL:
                        stats_GL = evo_pokemon_pvp.get_stat_product('GL', int(attack), int(defense), int(stamina))
                        stats['GL'] = stats_GL
                    if analyze_UL:
                        stats_UL = evo_pokemon_pvp.get_stat_product('UL', int(attack), int(defense), int(stamina))
                        stats['UL'] = stats_UL
                    if analyze_ML:
                        stats_ML = evo_pokemon_pvp.get_stat_product('ML', int(attack), int(defense), int(stamina))
                        stats['ML'] = stats_ML

                    power_up = pokemon_power_up.calc_evolve_cp(evo_pokemon.lower(), int(cp), int(attack), int(defense), int(stamina))

                results.append({
                    'inputs': inputs,
                    'stats': stats,
                    'power_up': power_up
                })

        # print(results)

        context = {
            'pokemon': req_pokemon,
            'evolution': evo_pokemon,
            'analyze_GL': analyze_GL,
            'analyze_UL': analyze_UL,
            'analyze_ML': analyze_ML,
            'results': results
        }
        return render(request, template, context)

    
def search(request, pokemon):
    # use provided string representing part of pokemon's name to search for matches in the BaseStats model
    # search for pokemon like Alolan Marowak by using ' ' + pokemon
    form_pokemon = ' ' + pokemon
    matches = BaseStats.objects.filter(species__istartswith=pokemon).order_by('species').values_list('species')
    # print('matches', matches)
    # returns a list of tuples: [('Charmander',), ('Charizard',)]
    matches = list(sum(matches, ()))
    form_matches = BaseStats.objects.filter(species__icontains=form_pokemon).values_list('species')
    # print('form matches', form_matches)
    form_matches = list(sum(form_matches, ()))

    # TODO: look up evolution 

    results = {'results': matches + form_matches}

    return JsonResponse(results)


def get_evolutions(request, pokemon):
    # use pokemon string to get list of its evolutions
    matches = EvolutionTable.objects.filter(species__iexact=pokemon.lower())

    if bool(matches):
        matches = matches.first().evolution
        print(matches)
        results = {'results': matches}
    else:
        # empty query set returned
        results = {'results': []}


    return JsonResponse(results)
