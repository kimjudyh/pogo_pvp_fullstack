from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .LeagueStats import LeagueStats

# Create your views here.

def home(request):
    pokemon = LeagueStats('skarmory')
    stats = pokemon.get_stat_product('GL', 12, 14, 15)
    # return JsonResponse(stats)

    template = 'home.html'
    return render(request, template)


def analyze(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.POST['pokemon'])

        req_pokemon = request.POST['pokemon']
        attack = request.POST['attack']
        defense = request.POST['defense']
        stamina = request.POST['stamina']

        pokemon = LeagueStats(req_pokemon.lower())
        stats = pokemon.get_stat_product('GL', attack, defense, stamina)

        template = 'home.html'
        context = {
            'pokemon': req_pokemon,
            'attack': attack,
            'defense': defense,
            'stamina': stamina,
            'stats': stats}
        return render(request, template, context)
        # return JsonResponse(stats)


        # return HttpResponse('<h1>yo</h1>')


    

