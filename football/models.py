from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
import os

class CompetitionManager(models.Manager):
	def rename_competition(self, competition_id, filename):
		competition = Competition.objects.get(pk=competition_id)
		return 'competitions/{0}.{1}'.format(competition.name, filename.rpartition('.')[len(filename.rpartition('.'))-1])

class Competition(models.Model):
	def competition_path(instance, filename):
		if filename:
			return 'competitions/{0}.{1}'.format(instance.name, filename.rpartition('.')[len(filename.rpartition('.'))-1])
		else:
			return ''

	competition_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	logo = models.ImageField(upload_to=competition_path, blank=True, default='')
	format_choices = (
		('l', 'League'),
		('k', 'Knockout'),
		#('g', 'Grouped'),
	)
	competition_format = models.CharField(max_length=1, choices=format_choices, default='l')
	promotion_limit = models.IntegerField(default=0)
	qualifying_limit = models.IntegerField(default=0)
	relegation_limit = models.IntegerField(default=0)

	objects = CompetitionManager()

	def rename(self, *args, **kwargs):
		if self.logo.name:
			filename = self.logo.name.rpartition('/')[len(self.logo.name.rpartition('/'))-1]
			name = filename.rpartition('.')[0]
			if not (name[0] == self.name):	#Check if the file is correctly named
				old_file = '{0}{1}'.format(settings.MEDIA_ROOT, self.logo.name)
				self.logo.name = Competition.objects.rename_competition(self.competition_id, self.logo.name)
				new_file = '{0}{1}'.format(settings.MEDIA_ROOT, self.logo.name)
				super().save(*args, **kwargs)
				os.replace(old_file, new_file)

	def save(self, *args, **kwargs):
			super().save(*args, **kwargs) # Call the "real" save() method
			self.rename()

	def __str__(self):
		return '%s' % (self.name)

# TODO Make Country model with choice selection and country names
# Source: http://www.fifa.com/associations/index.html

class Fixture(models.Model):
	fixture_id = models.AutoField(primary_key=True)
	season = models.ForeignKey('Season', on_delete=models.CASCADE)
	home_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name="fixtures")
	away_team = models.ForeignKey('Team', on_delete=models.CASCADE)
	location = models.ForeignKey('Venue', on_delete=models.CASCADE, null=True)
	date = models.DateField(auto_now=False, auto_now_add=False)
	time = models.TimeField(auto_now=False, auto_now_add=False)
	weather_choices = (
		('CLE', 'Clear'),
		('CLO', 'Cloudy'),
		('RAI', 'Rainy'),
		('OVE', 'Overcast'),
		('SUN', 'Sunny'),
		)
	weather = models.CharField(max_length=3, choices=weather_choices, default='CLE')
	temperature = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)	#Celsius
	windchill = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)	#Celsius
	humidity = models.IntegerField(null=True, blank=True)
	pressure = models.IntegerField(null=True, blank=True) #hPa
	wind_direction_choices = (
		('N', 'North'),
		('NNE', 'North-Northeast'),
		('NE', 'Northeast'),
		('ENE', 'East-Northeast'),
		('E', 'East'),
		('ESE', 'East-Southeast'),
		('SE', 'Southeast'),
		('SSE', 'South-Southeast'),
		('S', 'South'),
		('SSW', 'South-Southwest'),
		('SW', 'Southwest'),
		('WSW', 'West-Southwest'),
		('W', 'West'),
		('WNW', 'West-Northwest'),
		('NW', 'Northwest'),
		('NNW', 'North-Northwest'),
		('V', 'Variable'),
		('C', 'Calm')
		)
	wind_direction = models.CharField(max_length=3, choices=wind_direction_choices, default='C')
	wind_speed = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True) #km/H
	home_score = models.IntegerField(default=0)
	away_score = models.IntegerField(default=0)
	extra_time = models.BooleanField(default=False)
	penalty_shootout = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		if not self.location:
			self.location = self.home_team.venue
		super().save(*args, **kwargs) # Call the "real" save() method

		home_standing = TeamStanding.objects.save_standing(self.season, self.home_team)
		away_standing = TeamStanding.objects.save_standing(self.season, self.away_team)

	def __str__(self):
		return '%s - %s %d-%d %s' % (self.date, self.home_team, self.home_score, self.away_score, self.away_team)

class FixtureEvent(models.Model):
	event_id = models.AutoField(primary_key=True)
	event_choices = (
		('G', 'Goal'),
		('O', 'Own Goal'),
		('P', 'Penalty'),
		('R', 'Red Card'),
		('Y', 'Yellow Card')
		)
	event_type = models.CharField(max_length=1, choices=event_choices, default='G')
	fixture = models.ForeignKey('Fixture', on_delete=models.CASCADE)
	team = models.ForeignKey('Team', on_delete=models.CASCADE)
	player = models.ForeignKey('Player', on_delete=models.CASCADE)
	period_choices = (
		('1', '1st Half'),
		('2', '2nd Half'),
		('3', 'Overtime 1st Half'), 
		('4', 'Overtime 2nd Half'),
		('5', 'Penalty Shootout')
		)
	period = models.CharField(max_length=1, choices=period_choices, default='1')
	minute = models.IntegerField(default=0)

	def __str__(self):
		return '%s %s (%s - %s) - %s' % (self.player, self.event_type, self.period, self.minute, self.fixture)

class PlayerManager(models.Manager):
	def rename_player(self, player_id, filename):
		player = Player.objects.get(pk=player_id)
		return 'players/{0}/{1}.{2}'.format(player.nationality, player_id, filename.rpartition('.')[len(filename.rpartition('.'))-1])

class Player(models.Model):
	def player_path(instance, filename):
		if filename:
			if instance.player_id:
				return 'players/{0}/{1}.{2}'.format(instance.nationality, instance.player_id, filename.rpartition('.')[len(filename.rpartition('.'))-1])
			else:
				return 'players/{0}/{1}'.format(instance.nationality, filename)
		else:
			return ''

	player_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50, default='', blank=True)
	full_name = models.CharField(max_length=50)
	primary_positions = models.ManyToManyField(
		'Position',
		related_name="primary_positions")
	secondary_positions = models.ManyToManyField(
		'Position',
		related_name="secondary_positions", blank=True)
	club_number = models.IntegerField(default=0)
	country_number = models.IntegerField(default=0)
	dob = models.DateField(auto_now=False, auto_now_add=False)	#YYYY-MM-DD
	nationality = models.CharField(max_length=3)	#FIFA Country Code
	# TODO Make nationality foreign key with Country model
	current_team = models.ForeignKey('Team', on_delete=models.SET_DEFAULT, blank=True, default='')
	height = models.IntegerField()	#Centimeters
	weight = models.IntegerField()	#Kilograms
	portrait = models.ImageField(upload_to=player_path, blank=True, default='')

	objects = PlayerManager()

	def rename(self, *args, **kwargs):
		if self.portrait.name:
			filename = self.portrait.name.rpartition('/')[len(self.portrait.name.rpartition('/'))-1]
			country = self.portrait.name.rpartition('/')[len(self.portrait.name.rpartition('/'))-2]
			name = filename.rpartition('.')[0]
			if (not name[0] == self.player_id) or (not country == self.nationality):	#Check if the file is correctly named
				old_file = '{0}{1}'.format(settings.MEDIA_ROOT, self.portrait.name)
				self.portrait.name = Player.objects.rename_player(self.player_id, self.portrait.name)
				new_file = '{0}{1}'.format(settings.MEDIA_ROOT, self.portrait.name)
				super().save(*args, **kwargs)
				try:
					os.replace(old_file, new_file)
				except FileNotFoundError:
					# TODO
					pass
				except FileExistsError:
					# TODO
					pass

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs) # Call the "real" save() method
		self.rename()

	def __str__(self):
		return '%s %s' % (self.first_name, self.last_name)

class Position(models.Model):
	position_id = models.AutoField(primary_key=True)
	position = models.CharField(max_length=3)

	def __str__(self):
		return '%s' % (self.position)

class Season(models.Model):
	season_id = models.AutoField(primary_key=True)
	competition = models.ForeignKey('Competition', on_delete=models.CASCADE, related_name = 'seasons')
	year = models.IntegerField()	#Starting Year
	teams = models.ManyToManyField('Team')

	def years(self):
		return '%s-%s' % (self.year, (self.year+1))
		
	def __str__(self):
		return '%s %s-%s' % (self.competition.name, self.year, (self.year+1))

class TeamStandingManager(models.Manager):
	def save_standing(self, season, team):
		team_standing = TeamStanding
		exists = True
		if TeamStanding.objects.filter(season=season, team=team).count():
			team_standing = TeamStanding.objects.filter(season=season, team=team).get()
		else:
			exists = False

		team_standing.games_played = 0
		team_standing.wins = 0
		team_standing.losses = 0
		team_standing.draws = 0
		team_standing.overtime_wins = 0
		team_standing.overtime_losses = 0
		team_standing.goals_forced = 0
		team_standing.goals_allowed = 0
		team_standing.goal_difference = 0
		team_standing.points = 0

		# TODO - Logic for calculating streaks
		win_streak = 0
		win_draw_streak = 0
		draw_streak = 0
		draw_loss_streak = 0
		loss_streak = 0
		clean_sheet_streak = 0
		failed_to_score_streak = 0

		for fixture in Fixture.objects.filter(Q(season_id=season), Q(home_team=team) | Q(away_team=team)):
			team_standing.games_played += 1
			if (fixture.home_team == team and fixture.home_score > fixture.away_score) or (fixture.away_team == team and fixture.away_score > fixture.home_score):
				if(fixture.extra_time == True):
					team_standing.overtime_wins += 1
				team_standing.wins += 1
				team_standing.points += 3
			elif (fixture.away_team == team and fixture.home_score > fixture.away_score) or (fixture.home_team == team and fixture.away_score > fixture.home_score):
				if(fixture.extra_time == True):
					team_standing.overtime_losses += 1
				team_standing.losses += 1
			else:
				team_standing.draws += 1
				team_standing.points += 1
			if fixture.home_team == team:
				team_standing.goals_forced += fixture.home_score
				team_standing.goals_allowed += fixture.away_score
			if fixture.away_team == team:
				team_standing.goals_forced += fixture.away_score
				team_standing.goals_allowed += fixture.home_score
		team_standing.goal_difference = team_standing.goals_forced - team_standing.goals_allowed

		if exists:
			team_standing.save()
		else:
			team_standing = self.create(season=season, 
			team=team, games_played=team_standing.games_played, wins=team_standing.wins, losses=team_standing.losses, draws=team_standing.draws, overtime_wins=team_standing.overtime_wins, 
			overtime_losses=team_standing.overtime_losses, goals_forced=team_standing.goals_forced, goals_allowed=team_standing.goals_allowed, 
			goal_difference=team_standing.goal_difference, points=team_standing.points)
		
		return team_standing

class TeamStanding(models.Model):
	team_standing_id = models.AutoField(primary_key=True)
	season = models.ForeignKey('Season', on_delete=models.CASCADE, related_name='standings', blank=False)
	team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='standings', blank=False)
	games_played = models.IntegerField(default=0)
	wins = models.IntegerField(default=0)
	losses = models.IntegerField(default=0)
	draws = models.IntegerField(default=0)
	overtime_wins = models.IntegerField(default=0)
	overtime_losses = models.IntegerField(default=0)
	goals_forced = models.IntegerField(default=0)
	goals_allowed = models.IntegerField(default=0)
	goal_difference = models.IntegerField(default=0)
	points = models.IntegerField(default=0)
	win_streak = models.IntegerField(default=0)
	win_draw_streak = models.IntegerField(default=0)
	draw_streak = models.IntegerField(default=0)
	draw_loss_streak = models.IntegerField(default=0)
	loss_streak = models.IntegerField(default=0)
	clean_sheet_streak = models.IntegerField(default=0)
	failed_to_score_streak = models.IntegerField(default=0)

	objects = TeamStandingManager()

	def __str__(self):
		return "%s - %s" % (self.season, self.team)

class TeamManager(models.Manager):
	def rename_team(self, team_id, filename):
		team = Team.objects.get(pk=team_id)
		return 'teams/{0}/{1}.{2}'.format(team.venue.country, team_id, filename.rpartition('.')[len(filename.rpartition('.'))-1])

class Team(models.Model):
	def team_path(instance, filename):
		if filename:
			if instance.team_id:
				return 'teams/{0}/{1}.{2}'.format(instance.venue.country, instance.team_id, filename.rpartition('.')[len(filename.rpartition('.'))-1])
			else:
				return 'teams/{0}/{1}'.format(instance.venue.country, filename)
		else:
			return ''

	team_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	crest = models.ImageField(upload_to=team_path, blank=True, default='')
	venue = models.ForeignKey('Venue', on_delete=models.CASCADE)

	objects = TeamManager()

	def rename(self, *args, **kwargs):
		if self.crest.name:
			filename = self.crest.name.rpartition('/')[len(self.crest.name.rpartition('/'))-1]
			country = self.crest.name.rpartition('/')[len(self.crest.name.rpartition('/'))-2]
			name = filename.rpartition('.')[0]
			if (not name[0] == self.team_id) or (not country == self.venue.country):	#Check if the file is correctly named
				old_file = '{0}{1}'.format(settings.MEDIA_ROOT, self.crest.name)
				self.crest.name = Team.objects.rename_team(self.team_id, self.crest.name)
				new_file = '{0}{1}'.format(settings.MEDIA_ROOT, self.crest.name)
				super().save(*args, **kwargs)
				os.replace(old_file, new_file)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs) # Call the "real" save() method
		self.rename()

	def __str__(self):
		return '%s' % (self.name)

class VenueManager(models.Manager):
	def rename_venue(self, venue_id, filename):
		venue = Venue.objects.get(pk=venue_id)
		return 'venues/{0}/{1}.{2}'.format(venue.country, venue_id, filename.rpartition('.')[len(filename.rpartition('.'))-1])

class Venue(models.Model):
	def venue_path(instance, filename):
		if filename:
			if instance.venue_id:
				return 'venues/{0}/{1}.{2}'.format(instance.country, instance.venue_id, filename.rpartition('.')[len(filename.rpartition('.'))-1])
			else:
				return 'venues/{0}/{1}'.format(instance.country, filename)
		else:
			return ''

	venue_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	country = models.CharField(max_length=3) # TODO make foreign key to Country model
	altitude = models.IntegerField()	#Meters
	picture = models.ImageField(upload_to=venue_path, blank=True, default='')

	objects = VenueManager()

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs) # Call the "real" save() method
		if self.picture.name:
			filename = self.picture.name.rpartition('/')[len(self.picture.name.rpartition('/'))-1]
			country = self.picture.name.rpartition('/')[len(self.picture.name.rpartition('/'))-2]
			name = filename.rpartition('.')[0]
			if (not name[0] == self.venue_id) or (not country == self.country):	#Check if the file is correctly named
				old_file = '{0}{1}'.format(settings.MEDIA_ROOT, self.picture.name)
				self.picture.name = Venue.objects.rename_venue(self.venue_id, self.picture.name)
				new_file = '{0}{1}'.format(settings.MEDIA_ROOT, self.picture.name)
				# super().save(*args, **kwargs)
				os.replace(old_file, new_file)

	def __str__(self):
		return '%s' % (self.name)

#Fixture Statistics Models
class Statistics(models.Model):
	fixture_id = models.ForeignKey('Fixture', on_delete=models.CASCADE)
	player_id = models.ForeignKey('Player', on_delete=models.CASCADE)
	#General Stats
	minute_in = models.IntegerField(default=0)
	minute_out = models.IntegerField(default=90)
	yellow_cards = models.IntegerField(default=0)
	red_cards = models.IntegerField(default=0)
	#Offensive Stats
	goals = models.IntegerField(default=0)
	assists = models.IntegerField(default=0)
	shots = models.IntegerField(default=0)
	shots_on_target = models.IntegerField(default=0)
	shots_blocked = models.IntegerField(default=0)
	crossbar = models.IntegerField(default=0)
	touches = models.IntegerField(default=0)
	dribbles_attempted = models.IntegerField(default=0)
	dribbles_won = models.IntegerField(default=0)
	fouled = models.IntegerField(default=0)
	offsides = models.IntegerField(default=0)
	possession = models.DecimalField(default=0, max_digits=3, decimal_places=1)
	dispossessed = models.IntegerField(default=0)
	#Passing Stats
	passes = models.IntegerField(default=0)
	key_passes = models.IntegerField(default=0)
	pass_accuracy = models.DecimalField(default=0, max_digits=4, decimal_places=1)
	crosses = models.IntegerField(default=0)
	accurate_crosses = models.IntegerField(default=0)
	corners = models.IntegerField(default=0)
	corner_accuracy = models.DecimalField(default=0, max_digits=4, decimal_places=1)
	long_balls = models.IntegerField(default=0)
	accurate_long_balls = models.IntegerField(default=0)
	through_balls = models.IntegerField(default=0)
	accurate_through_balls = models.IntegerField(default=0)
	defensive_aerials = models.IntegerField(default=0)
	offensive_aerials = models.IntegerField(default=0)
	aerials_won = models.IntegerField(default=0)
	#Defensive Stats
	total_tackles = models.IntegerField(default=0)
	successful_tackles = models.IntegerField(default=0)
	interceptions = models.IntegerField(default=0)
	dribbled_past = models.IntegerField(default=0)
	clearances = models.IntegerField(default=0)
	blocked_shots = models.IntegerField(default=0)
	fouls_committed = models.IntegerField(default=0)
	saves = models.IntegerField(default=0)

	def __str__(self):
		return '%s statistics for %s' % (self.player_id, self.fixture_id)
