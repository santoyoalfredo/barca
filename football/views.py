from django.shortcuts import render

# Create your views here.
from .models import Player


def index(request):
	player_list = Player.objects.all().order_by('club_number')
	context = {
        'players': player_list,
    }
	return render(request, 'football/index.html', context)