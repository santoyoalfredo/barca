from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import *
from datetime import date

# Create your views here.
from .models import *
from .forms import *

class CompetitionAddView(FormView):
	template_name = 'football/competitions_add.html'
	form_class = CompetitionAddForm
	success_url = reverse_lazy('competitions')

	def form_valid(self, form):
		form.add_competition()
		print('Added competition')
		return super().form_valid(form)

class CompetitionEditView(UpdateView):
	model = Competition
	template_name = 'football/competitions_add.html'
	form_class = CompetitionAddForm
	success_url = reverse_lazy('competitions')

	def form_valid(self, form):
		return super().form_valid(form)

class CompetitionDeleteView(DeleteView):
	model = Competition
	success_url = reverse_lazy('competitions')

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

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['positions'] = list(Position.objects.all().order_by('position'))
		return context

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
