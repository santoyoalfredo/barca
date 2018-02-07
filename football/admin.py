from django.contrib import admin

# Register your models here.
from .models import Player

class PlayerAdmin(admin.ModelAdmin):
	fields = ['name', 'full_name', 'position', 'dob', 'nationality', 'current_team', 'height', 'weight']
	list_display = ('name', 'position', 'dob', 'nationality', 'current_team', 'height', 'weight', 'player_id')

admin.site.register(Player, PlayerAdmin)