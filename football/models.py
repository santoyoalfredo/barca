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
	temperature = models.DecimalField(max_digits=3, decimal_places=1)
	windchill = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
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
		return '%s %d-%d %s' % (self.home_team, self.home_score, self.away_score, self.away_team)

class Player(models.Model):
	player_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	full_name = models.CharField(max_length=50)
	position = models.CharField(max_length=3)
	club_number = models.IntegerField(default=0)
	country_number = models.IntegerField(default=0)
	dob = models.DateField(auto_now=False, auto_now_add=False)
	nationality = models.CharField(max_length=3)
	current_team = models.ForeignKey('Team', on_delete=models.SET_DEFAULT, blank=True, default='')
	height = models.IntegerField()
	weight = models.IntegerField()
	portrait = models.ImageField(upload_to='resources/players/', null=True, blank=True, default='')

	def __str__(self):
		return '%s' % (self.name)

class Season(models.Model):
	season_id = models.AutoField(primary_key=True)
	competition_id = models.ForeignKey('Competition', on_delete=models.SET_DEFAULT, blank=True, default='')
	year = models.IntegerField()
	teams = models.ManyToManyField('Team')

	def __str__(self):
		return '%s %s-%s' % (self.competition_id, self.year, (self.year+1))

class Team(models.Model):
	team_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	venue = models.ForeignKey('Venue', on_delete=models.SET_DEFAULT, blank=True, default='')

	def __str__(self):
		return '%s' % (self.name)

class Venue(models.Model):
	venue_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	country = models.CharField(max_length=3)
	altitude = models.IntegerField()

	def __str__(self):
		return '%s' % (self.name)

