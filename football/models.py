from django.db import models

# Create your models here.
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

