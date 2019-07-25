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

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['competitions'] = Competition.objects.all().order_by('name')
		return context

class FixtureView(generic.TemplateView):
	model = Fixture
	template_name = 'football/fixture_detail.html'

	def calculateMinuteDif(self, minute):
		minuteDif = minute - 45
		return str(minute - minuteDif) + "+" + str(minuteDif) + "'"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		events = FixtureEvent.objects.filter(fixture=context['pk']).order_by('period', 'minute')
		fixture = Fixture.objects.get(pk=context['pk'])

		# Create a dictionary of events with the player as a key to group events by player
		homeEvents = dict()
		awayEvents = dict()
		homeRedEvents = dict()
		awayRedEvents = dict()
		homeEvent = True
		
		for event in events:			
			#Event in added time of second half of overtime 
			if event.period == '4' and event.minute > 90:
				eventString = self.calculateMinuteDif(event.minute)
			#Event in added time of first half of overtime 
			if event.period == '3' and event.minute > 90:
				eventString = self.calculateMinuteDif(event.minute)
			#Event in added time of second half 
			if event.period == '2' and event.minute > 90:
				eventString = self.calculateMinuteDif(event.minute)
			#Event in added time of first half 
			elif event.period == '1' and event.minute > 45:
				eventString = self.calculateMinuteDif(event.minute)
			else:
				eventString = str(event.minute) + "'"

			if event.event_type == 'P':
				eventString += " (P)"
			
			if event.event_type == 'O':
				eventString += " (OG)"

			if event.team == fixture.home_team and (event.event_type == "G" or event.event_type == "P"):
				homeEvent = True
			elif event.team == fixture.away_team and event.event_type == "O":
				homeEvent = True
			if event.team == fixture.away_team and (event.event_type == "G" or event.event_type == "P"):
				homeEvent = False
			elif event.team == fixture.home_team and event.event_type == "O":
				homeEvent = False

			if homeEvent:
				if event.event_type == 'R':
					homeRedEvents[event.player] = eventString
				elif not event.player in homeEvents:
					homeEvents[event.player] = [eventString]
				else:
					homeEvents[event.player].append(eventString)
			else:
				if event.event_type == 'R':
					awayRedEvents[event.player] = eventString
				elif not event.player in awayEvents:
					awayEvents[event.player] = [eventString]
				else:
					awayEvents[event.player].append(eventString)

		context['homeEvents'] = homeEvents
		context['awayEvents'] = awayEvents
		context['homeRedEvents'] = homeRedEvents
		context['awayRedEvents'] = awayRedEvents
		context['fixture'] = fixture
		context['stats'] = Statistics.objects.filter(fixture_id=context['pk'])
		return context

class PlayerListView(generic.ListView):
	model = Player
	template_name = 'football/player_list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['players'] = Player.objects.all().order_by('last_name', 'first_name')
		return context

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
