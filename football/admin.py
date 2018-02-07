from django.contrib import admin

# Register your models here.
from .models import *

class CompetitionAdmin(admin.ModelAdmin):
	fields = ['name', 'logo']
	list_display = ('name', 'competition_id')

class FixtureAdmin(admin.ModelAdmin):
	fields = ['season_id', 'home_team', 'away_team', 'home_score', 'away_score', 'extra_time', 'penalty_shootout', 'location',
	 'time', 'date', 'weather', 'temperature', 'windchill', 'humidity', 'pressure', 'wind_direction', 'wind_speed']
	list_display = ('fixture_id' , 'home_team', 'home_score', 'away_team', 'away_score', 'date', 'season_id')
	list_editable = ('home_score', 'away_score')

class PlayerAdmin(admin.ModelAdmin):
	fields = ['name', 'full_name', 'position', 'dob', 'current_team', 'club_number', 'nationality', 'height', 'weight', 'portrait']
	list_display = ('name', 'current_team', 'club_number', 'position', 'dob', 'nationality', 'height', 'weight', 'player_id')
	list_editable = ('club_number', 'height', 'weight')

class SeasonAdmin(admin.ModelAdmin):
	fields = ['competition_id', 'year', 'teams']
	list_display = ('competition_id', 'year')

class TeamAdmin(admin.ModelAdmin):
	fields = ['name', 'venue']
	list_display = ('name', 'venue', 'team_id')

class VenueAdmin(admin.ModelAdmin):
	fields = ['name', 'city', 'country', 'altitude']
	list_display = ('name', 'city', 'country', 'altitude', 'venue_id')

admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Fixture, FixtureAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Venue, VenueAdmin)