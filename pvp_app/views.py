from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .LeagueStats import LeagueStats

# Create your views here.

def home(request):
    template = 'home.html'
    return render(request, template)


def analyze(request):
    if request.method == 'POST':
        print(request.POST)

        # deal with multiple entries

        req_pokemon = request.POST['pokemon']
        pokemon = LeagueStats(req_pokemon.lower())
        stats_array = []

        # need to use getlist to save all values, otherwise will default to giving just last value
        a = request.POST.getlist('attack')
        d = request.POST.getlist('defense')
        s = request.POST.getlist('stamina')
        print(a, d, s)

        # multiple entries: 'attack': [1, 3, 6] etc.
        for attack, defense, stamina in zip(a, d, s):
            if attack != '' and defense != '' and stamina != '':
                stats = pokemon.get_stat_product('GL', attack, defense, stamina)
                stats['attack'] = attack
                stats['defense'] = defense
                stats['stamina'] = stamina
                stats_array.append(stats)
                print(stats_array)


        # attack = request.POST['attack']
        # defense = request.POST['defense']
        # stamina = request.POST['stamina']

        # stats = pokemon.get_stat_product('GL', attack, defense, stamina)

        template = 'home.html'
        context = {
            'pokemon': req_pokemon,
            'attack': request.POST['attack'],
            'defense': request.POST['defense'],
            'stamina': request.POST['stamina'],
            'stats_array': stats_array}
        return render(request, template, context)
        # return JsonResponse(stats)


        # return HttpResponse('<h1>yo</h1>')


    

