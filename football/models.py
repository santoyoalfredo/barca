from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q

# Create your models here.
class Competition(models.Model):
	competition_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	logo = models.ImageField(upload_to='resources/competitions/', blank=True, default='')

	def __str__(self):
		return '%s' % (self.name)

class Fixture(models.Model):
	fixture_id = models.AutoField(primary_key=True)
	season_id = models.ForeignKey('Season', on_delete=models.SET_NULL, null=True)
	home_team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, related_name="home_team")
	away_team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, related_name="away_team")
	location = models.ForeignKey('Venue', on_delete=models.SET_NULL, null=True)
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
	temperature = models.DecimalField(max_digits=3, decimal_places=1)	#Celsius
	windchill = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)	#Celsius
	humidity = models.IntegerField()
	pressure = models.IntegerField() #hPa
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
	wind_speed = models.DecimalField(max_digits=3, decimal_places=1) #km/H
	home_score = models.IntegerField(default=0)
	away_score = models.IntegerField(default=0)
	extra_time = models.BooleanField(default=False)
	penalty_shootout = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		home_standing = TeamStanding.objects.save_standing(self.season_id, self.home_team)
		# create_away_team_standing_instance_without_streaks
		away_standing = TeamStanding.objects.save_standing(self.season_id, self.away_team)
		super().save(*args, **kwargs) # Call the "real" save() method

	def __str__(self):
		return '%s - %s - %s %d-%d %s' % (self.season_id, self.date, self.home_team, self.home_score, self.away_score, self.away_team)

class Player(models.Model):
	player_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50, default='', blank=True)
	full_name = models.CharField(max_length=50)
	positions = models.ManyToManyField('Position')
	club_number = models.IntegerField(default=0)
	country_number = models.IntegerField(default=0)
	dob = models.DateField(auto_now=False, auto_now_add=False)	#YYYY-MM-DD
	nationality = models.CharField(max_length=3)	#FIFA Country Code
	current_team = models.ForeignKey('Team', on_delete=models.SET_DEFAULT, blank=True, default='')
	height = models.IntegerField()	#Centimeters
	weight = models.IntegerField()	#Kilograms
	portrait = models.ImageField(upload_to='resources/players/', null=True, blank=True, default='')

	def __str__(self):
		return '%s %s' % (self.first_name, self.last_name)

class Position(models.Model):
	position_id = models.AutoField(primary_key=True)
	position = models.CharField(max_length=3)

	def __str__(self):
		return '%s' % (self.position)

class Season(models.Model):
	season_id = models.AutoField(primary_key=True)
	competition = models.ForeignKey('Competition', on_delete=models.SET_DEFAULT, related_name = 'seasons', blank=True, default='')
	year = models.IntegerField()	#Starting Year
	teams = models.ManyToManyField('Team')

	def years(self):
		return '%s-%s' % (self.year, (self.year+1))
		
	def __str__(self):
		return '%s %s-%s' % (self.competition_id, self.year, (self.year+1))

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

		for fixture in Fixture.objects.filter(Q(season_id=season), Q(home_team=team) | Q(away_team=team)):
			team_standing.games_played += 1
			if (fixture.home_team == team and fixture.home_score > fixture.away_score) or (fixture.away_team == team and fixture.away_score > fixture.home_score):
				if(fixture.extra_time == True):
					team_standing.overtime_wins += 1
				team_standing.wins += 1
				team_standing.points += 3
			elif (fixture.away_team == team and fixture.home_score < fixture.away_score) or (fixture.away_team == team and fixture.away_score < fixture.home_score):
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
			goal_difference=team_standing.goal_difference,points=team_standing.points)
		
		return team_standing

class TeamStanding(models.Model):
	team_standing_id = models.AutoField(primary_key=True)
	season = models.ForeignKey('Season', on_delete=models.CASCADE, related_name='standings', blank=False)
	team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='standings', blank=False)
	#position = models.IntegerField()
	games_played = models.IntegerField(default=0)
	wins = models.IntegerField(default=0)
	losses = models.IntegerField(default=0)
	draws = models.IntegerField(default=0)
	overtime_wins = models.IntegerField(default=0)
	overtime_losses = models.IntegerField(default=0)
	#winningPercentage
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

class Team(models.Model):
	team_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	crest = models.ImageField(upload_to='resources/teams', null=True, blank=True, default='')
	venue = models.ForeignKey('Venue', on_delete=models.SET_DEFAULT, blank=True, default='')

	def __str__(self):
		return '%s' % (self.name)

class Venue(models.Model):
	venue_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	country = models.CharField(max_length=3)
	altitude = models.IntegerField()	#Meters

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

	def __str__(self):
		return '%s statistics for %s' % (self.player_id, self.fixture_id)