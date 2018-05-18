from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import *
from datetime import date

from .models import *
from .forms import *

class CompetitionAddView(FormView):
	template_name = 'football/competition_add.html'
	form_class = CompetitionAddForm
	success_url = reverse_lazy('competitions')

	def form_valid(self, form):
		form.add_competition()
		print('Added competition')
		return super().form_valid(form)

class CompetitionEditView(UpdateView):
	model = Competition
	template_name = 'football/competition_add.html'
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

class FixtureView(generic.TemplateView):
	model = Fixture
	template_name = 'football/fixture_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# TODO - Create dict of events to consolidate goals from the same player
		# TODO - Order dict of events chronologically
		context['events'] = FixtureEvent.objects.filter(fixture=context['pk']).order_by('period', 'minute')
		context['fixture'] = Fixture.objects.get(pk=context['pk'])
		context['stats'] = Statistics.objects.filter(fixture_id=context['pk'])
		return context

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

class PlayerAddView(FormView):
	template_name = 'football/player_add.html'
	form_class = PlayerAddForm
	success_url = reverse_lazy('players')

	def form_valid(self, form):
		form.add_player()
		return super().form_valid(form)

class PlayerEditView(UpdateView):
	model = Player
	template_name = 'football/player_add.html'
	form_class = PlayerAddForm
	success_url = reverse_lazy('players')

	def form_valid(self, form):
		return super().form_valid(form)

class PlayerDeleteView(DeleteView):
	model = Player
	success_url = reverse_lazy('players')

class SeasonView(generic.TemplateView):
	model = Season
	template_name = 'football/season_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['season'] = Season.objects.get(pk=context['pk'])
		context['standings'] = TeamStanding.objects.filter(season=self.kwargs['pk']).order_by('-points','-goal_difference','-goals_forced')
		context['fixtures'] = Fixture.objects.filter(season=self.kwargs['pk']).order_by('date','time', 'home_team')
		return context
	
class SeasonAddView(FormView):
	template_name = 'football/season_add.html'
	form_class = SeasonAddForm
	success_url = reverse_lazy('competitions')

	def form_valid(self, form):
		form.add_season()
		return super().form_valid(form)

	def get_initial(self):
		return {'competition': self.kwargs['competition_id']}

class SeasonEditView(UpdateView):
	model = Season
	template_name = 'football/season_add.html'
	form_class = SeasonAddForm
	success_url = reverse_lazy('season')

	def form_valid(self, form):
		return super().form_valid(form)

class SeasonDeleteView(DeleteView):
	model = Season
	success_url = reverse_lazy('competitions')

def index(request):
	return render(request, 'football/index.html')
