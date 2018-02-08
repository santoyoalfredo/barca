from django.shortcuts import render

# Create your views here.
from .models import Player, Statistics


def index(request):
	player_list = Player.objects.all().order_by('club_number')
	stats_list = Statistics.objects.all()
	context = {
        'players': player_list,
        'statistics': stats_list,
    }
	return render(request, 'football/index.html', context)