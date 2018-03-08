from django.shortcuts import get_object_or_404, render
from django.views import generic
from datetime import date

# Create your views here.
from .models import *

class CompetitionListView(generic.ListView):
	model = Competition
	template_name = 'football/competitions.html'

	def competitions(self):
		return Competition.objects.all().order_by('name')

class PlayerListView(generic.ListView):
	model = Player
	template_name = 'football/player_list.html'

	def players(self):
		return Player.objects.all().order_by('last_name', 'first_name')

class PlayerView(generic.DetailView):
	model = Player
	template_name = 'football/player_detail.html'
	def age(self):
		age = date.today() - self.object.dob
		return int(age.days / 365)

	def imp_height(self):
		inches = (self.object.height * 0.393701)
		feet = int(inches / 12)
		inches = int(inches % 12)
		return [feet, inches]

	def imp_weight(self):
		return int(self.object.weight * 2.20462)

	def positions(self):
		positions = []
		for pos in Position.objects.all():
			if (self.object.positions.filter(position=pos)) : positions.append(1)
			else: positions.append(0)
		return positions

class SeasonView(generic.TemplateView):
	model = Season
	template_name = 'football/season_detail.html'

	def season(self):
		season = self.kwargs['season_id']
		return Season.objects.get(pk=season)

	def standings(self):
		return TeamStanding.objects.filter(season=self.kwargs['season_id']).order_by('-points','-goal_difference','-goals_forced')
	
def index(request):
	return render(request, 'football/index.html')