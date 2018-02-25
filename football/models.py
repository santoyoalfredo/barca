from django.db import models

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
	pressure = models.IntegerField()
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
		)
	wind_direction = models.CharField(max_length=3, choices=wind_direction_choices, default='V')
	wind_speed = models.DecimalField(max_digits=3, decimal_places=1)
	home_score = models.IntegerField()
	away_score = models.IntegerField()
	extra_time = models.BooleanField()
	penalty_shootout = models.BooleanField()

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
	competition_id = models.ForeignKey('Competition', on_delete=models.SET_DEFAULT, related_name = 'seasons', blank=True, default='')
	year = models.IntegerField()	#Starting Year
	teams = models.ManyToManyField('Team')

	def __str__(self):
		return '%s %s-%s' % (self.competition_id, self.year, (self.year+1))

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