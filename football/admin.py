from django.contrib import admin

# Register your models here.
from .models import *

class CompetitionAdmin(admin.ModelAdmin):
	list_display = ('name', 'competition_id')

class FixtureAdmin(admin.ModelAdmin):
	fields = ['season_id', 'home_team', 'away_team', 'home_score', 'away_score', 'extra_time', 'penalty_shootout', 'location',
	 'time', 'date', 'weather', 'temperature', 'windchill', 'humidity', 'pressure', 'wind_direction', 'wind_speed']
	list_display = ('fixture_id' , 'home_team', 'home_score', 'away_team', 'away_score', 'date', 'season_id')
	list_editable = ('home_score', 'away_score')
	list_filter = ('season_id',)
	ordering = ('season_id', 'date')
	search_fields = ['home_team__name', 'away_team__name']

class PlayerAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': (('first_name', 'last_name'), 'full_name', 'positions', 'dob', ('current_team', 'club_number'), 
				'nationality', ('height', 'weight'), 'portrait')
		}),
	)
	list_display = ('first_name', 'last_name', 'current_team', 'club_number', 'dob', 'nationality', 'height', 'weight', 'player_id')
	list_editable = ('club_number', 'height', 'weight')
	ordering = ('last_name', 'first_name')

class PositionAdmin(admin.ModelAdmin):
	fields = ['position']
	list_display = ('position',)

class SeasonAdmin(admin.ModelAdmin):
	fields = ['competition_id', 'year', 'teams']
	list_display = ('competition_id', 'year')
	filter_horizontal = ('teams',)

class StatisticsAdmin(admin.ModelAdmin):
	fieldsets = (
		('General', {
			'fields': ('fixture_id', 'player_id', ('minute_in', 'minute_out', 'yellow_cards', 'red_cards'))
		}),
		('Offensive Stats', {
			'fields': (('shots', 'shots_on_target', 'shots_blocked', 'crossbar'), ('touches', 'dribbles_attempted', 
				'dribbles_won', 'fouled'), ('offsides','possession', 'dispossessed'),)
		}),
		('Passing Stats', {
			'fields': (('passes', 'key_passes', 'pass_accuracy', 'crosses'), ('accurate_crosses', 'corners', 
				'corner_accuracy', 'long_balls'), ('accurate_long_balls', 'through_balls', 'accurate_through_balls', 
				'defensive_aerials'), ('offensive_aerials', 'aerials_won'),)
		}),
		('Defensive Stats', {
			'fields': (('total_tackles', 'successful_tackles', 'interceptions', 'dribbled_past'), ('clearances', 
				'blocked_shots', 'fouls_committed'),)
		}),
	)
	list_display = ('fixture_id', 'player_id')

class TeamStandingAdmin(admin.ModelAdmin):
	pass

class TeamAdmin(admin.ModelAdmin):
	fields = ['name', 'venue', 'crest']
	list_display = ('name', 'venue', 'team_id')
	ordering = ('name',)

class VenueAdmin(admin.ModelAdmin):
	fields = ['name', 'city', 'country', 'altitude']
	list_display = ('name', 'city', 'country', 'altitude', 'venue_id')

admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Fixture, FixtureAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamStanding, TeamStandingAdmin)
admin.site.register(Venue, VenueAdmin)
