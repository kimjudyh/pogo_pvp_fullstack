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
        max_level   = request.POST['max_level']

        # get stat product for the requested evolution pokemon
        pokemon_power_up = PowerUpStats(req_pokemon.lower())
        matches = [evo_pokemon.lower()]
        if evo_pokemon.lower() == "all":
            found_match = EvolutionTable.objects.filter(species__iexact=req_pokemon.lower())
            if bool(found_match):
                matches = found_match.first().evolution
            else:
                matches = []

            target_evolutions = []
            for evo in matches:
                target_evolutions.append(LeagueStats(evo.lower()))
        else:
            target_evolutions = [LeagueStats(evo_pokemon.lower())]

        print('first target evolutions', target_evolutions)
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
        evo_species_is_valid = True
        for evo_pokemon_pvp in target_evolutions:
            # evo_species_is_valid &= evo_pokemon_pvp.verify_evo_pokemon()
            print('evo pokemon', evo_pokemon_pvp.pokemon)
            print('evo valid in loop', evo_species_is_valid)
            evo_species_is_valid = evo_species_is_valid and evo_pokemon_pvp.verify_evo_pokemon()
        print('evo valid', evo_species_is_valid)
        if not evo_species_is_valid:
            context = {
                'pokemon': req_pokemon,
                'evolution': evo_pokemon,
                'error': f'Invalid Evolution: {evo_pokemon}'
            }
            return render(request, template, context)
        
        # check for valid max level input (40 <= max_level <= 51)
        if float(max_level) < 40 or float(max_level) > 51:
            context = {
                'pokemon': req_pokemon,
                'evolution': evo_pokemon,
                'error': f'Invalid Max Level: {max_level}'
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
                    print('target evolutions', target_evolutions)


                    if analyze_GL:
                        stats['GL'] = []
                        for evo_pokemon_pvp in target_evolutions:
                            stats_GL = evo_pokemon_pvp.get_stat_product('GL', int(attack), int(defense), int(stamina), float(max_level))
                            # stats['GL'][evo_pokemon_pvp.pokemon] = stats_GL
                            stats_GL['evo'] = evo_pokemon_pvp.pokemon
                            print('stats GL in loop', stats_GL)
                            stats['GL'].append(stats_GL)
                    if analyze_UL:
                        for evo_pokemon_pvp in target_evolutions:
                            stats_UL = evo_pokemon_pvp.get_stat_product('UL', int(attack), int(defense), int(stamina), float(max_level))
                            stats['UL'][evo_pokemon_pvp.pokemon] = stats_UL
                    if analyze_ML:
                        for evo_pokemon_pvp in target_evolutions:
                            stats_ML = evo_pokemon_pvp.get_stat_product('ML', int(attack), int(defense), int(stamina), float(max_level))
                            stats['ML'][evo_pokemon_pvp.pokemon] = stats_ML

                    power_up = pokemon_power_up.calc_evolve_cp(evo_pokemon.lower(), int(cp), int(attack), int(defense), int(stamina), float(max_level))

                print('power_up', power_up)
                print('stats', stats)
                results.append({
                    'inputs': inputs,
                    'stats': stats,
                    'power_up': power_up
                })

        # print(results)

        context = {
            'pokemon': req_pokemon,
            'evolution': evo_pokemon,
            'evolution_names': matches,
            'max_level': max_level,
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


def empty_search(request):
    results = {'results': []}
    return JsonResponse(results)


def empty_evolution(request):
    results = {'results': []}
    return JsonResponse(results)
