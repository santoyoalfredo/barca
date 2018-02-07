from django.contrib import admin

# Register your models here.
from .models import Player, Team, Venue

class PlayerAdmin(admin.ModelAdmin):
	fields = ['name', 'full_name', 'position', 'dob', 'current_team', 'club_number', 'nationality', 'height', 'weight', 'portrait']
	list_display = ('name', 'current_team', 'club_number', 'position', 'dob', 'nationality', 'height', 'weight', 'player_id')
	list_editable = ('club_number', 'height', 'weight')

class TeamAdmin(admin.ModelAdmin):
	fields = ['name', 'venue']
	list_display = ('name', 'venue', 'team_id')

class VenueAdmin(admin.ModelAdmin):
	fields = ['name', 'city', 'country', 'altitude']
	list_display = ('name', 'city', 'country', 'altitude', 'venue_id')

admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Venue, VenueAdmin)