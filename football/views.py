from django.shortcuts import get_object_or_404, render
from django.views import generic

# Create your views here.
from .models import Player, Statistics, Team

class PlayerListView(generic.ListView):
	model = Player
	template_name = 'football/player_list.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['players'] = Player.objects.all()
		return context

class PlayerView(generic.DetailView):
	model = Player
	template_name = 'football/player_detail.html'

def index(request):
	return render(request, 'football/index.html')