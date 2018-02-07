from django.db import models

# Create your models here.
class Player(models.Model):
	player_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	full_name = models.CharField(max_length=50)
	position = models.CharField(max_length=3)
	dob = models.DateField(auto_now=False, auto_now_add=False)
	nationality = models.CharField(max_length=3)
	current_team = models.CharField(max_length=50)
	height = models.IntegerField()
	weight = models.IntegerField()
