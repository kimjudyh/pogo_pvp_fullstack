from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .LeagueStats import LeagueStats
from .PowerUpStats import PowerUpStats
from .models import BaseStats, EvolutionTable

# Create your views here.

def home(request):
    template = 'home.html'
    return render(request, template)


def decorate(tag):
    emojis = ''
    if 'shiny' in tag.lower():
        emojis += '✨'
    if 'shadow' in tag.lower():
        emojis += '😈'
    if 'purified' in tag.lower() or 'pure' in tag.lower():
        emojis += '😇'
    if 'xxl' in tag.lower():
        emojis += '🦒'
    if 'xxs' in tag.lower():
        emojis += '🐭'
    return emojis + tag + emojis.reverse()

def analyze(request):
    if request.method == 'GET':
        return redirect('home')
    elif request.method == 'POST':
        template = 'home.html'

        # deal with multiple entries

        req_pokemon = request.POST['pokemon'].strip()
        evo_pokemon = request.POST['evo-pokemon'].strip()
        max_level   = request.POST['max_level']

        # get stat product for the requested evolution pokemon
        pokemon_power_up = PowerUpStats(req_pokemon.lower())
        # `matches` is the list of evolution pokemon
        matches = [evo.strip() for evo in evo_pokemon.lower().split(',')]
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
            target_evolutions = []
            for evo in matches:
                target_evolutions.append(LeagueStats(evo))

        print('first target evolutions', target_evolutions)
        # check for valid Pokemon input
        species_is_valid = pokemon_power_up.verify_pokemon()
        
        # check for valid evolution Pokemon input
        evo_species_is_valid = True
        for evo_pokemon_pvp in target_evolutions:
            evo_species_is_valid = evo_species_is_valid and evo_pokemon_pvp.verify_evo_pokemon()
        
        # check for valid max level input (40 <= max_level <= 51)
        max_level_valid = True
        if float(max_level) < 40 or float(max_level) > 51:
            max_level_valid = False

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
        t = request.POST.getlist('tag')
        # print(c, a, d, s)

        # multiple entries: 'attack': [1, 3, 6] etc.
        for cp, attack, defense, stamina, tag in zip(c, a, d, s, t):
            stats = {}
            inputs = {}

            if cp != '' and attack != '' and defense != '' and stamina != '':
                # save inputs so they can be used in template to fill out form
                inputs['attack'] = attack
                inputs['defense'] = defense
                inputs['stamina'] = stamina
                inputs['cp'] = cp
                inputs['tag'] = decorate(tag)

                # verify IVs and CP
                is_valid = True
                if species_is_valid:
                    is_valid = pokemon_power_up.verify_IV_inputs(int(cp), int(attack), int(defense), int(stamina))

                inputs['is_valid'] = is_valid

                if not is_valid or not evo_species_is_valid or not max_level_valid or not species_is_valid:
                    # mark this entry as wrong to display on html
                    # print('invalid')
                    power_up = {}
                    one_result = []
                else:
                    # proceed
                    print('target evolutions', target_evolutions)
                    one_result = []
                    for evo_pokemon_pvp in target_evolutions:
                        per_evolution = {'evo': evo_pokemon_pvp.pokemon, 'stats': {}, 'power_up': {}}
                        if analyze_GL:
                            stats_GL = evo_pokemon_pvp.get_stat_product('GL', int(attack), int(defense), int(stamina), float(max_level))
                            per_evolution['stats']['GL'] = stats_GL
                        if analyze_UL:
                            stats_UL = evo_pokemon_pvp.get_stat_product('UL', int(attack), int(defense), int(stamina), float(max_level))
                            per_evolution['stats']['UL'] = stats_UL
                        if analyze_ML:
                            stats_ML = evo_pokemon_pvp.get_stat_product('ML', int(attack), int(defense), int(stamina), float(max_level))
                            per_evolution['stats']['ML'] = stats_ML
                        # calc power up for each evo, add to array
                        power_up_loop = pokemon_power_up.calc_evolve_cp(evo_pokemon_pvp.pokemon.lower(), int(cp), int(attack), int(defense), int(stamina), float(max_level))
                        # add starting level to inputs dic
                        inputs['starting_level'] = power_up_loop['GL']['starting_level']
                        # power_up.append(power_up_loop)
                        per_evolution['power_up'] = power_up_loop
                        one_result.append(per_evolution)

                # print('stats', stats)
                results.append({
                    'inputs': inputs,
                    'outputs': one_result
                })

        # print(results)
        if not species_is_valid:
            context = {
                'pokemon': req_pokemon,
                'evolution': evo_pokemon,
                'max_level': max_level,
                'analyze_GL': analyze_GL,
                'analyze_UL': analyze_UL,
                'analyze_ML': analyze_ML,
                'results': results,
                'error': f'Invalid Pokemon: {req_pokemon}'
            }
            return render(request, template, context)

        if not evo_species_is_valid:
            context = {
                'pokemon': req_pokemon,
                'evolution': evo_pokemon,
                'max_level': max_level,
                'analyze_GL': analyze_GL,
                'analyze_UL': analyze_UL,
                'analyze_ML': analyze_ML,
                'results': results,
                'error': f'Invalid Evolution: {evo_pokemon}'
            }
            return render(request, template, context)
        
        if not max_level_valid:
            context = {
                'pokemon': req_pokemon,
                'evolution': evo_pokemon,
                'max_level': max_level,
                'analyze_GL': analyze_GL,
                'analyze_UL': analyze_UL,
                'analyze_ML': analyze_ML,
                'results': results,
                'error': f'Invalid Max Level: {max_level}'
            }
            return render(request, template, context)

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
