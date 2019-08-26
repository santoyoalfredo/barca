from django.test import TestCase
from django.urls import reverse_lazy

from football.models import *

class PlayerEditTests(TestCase):

    def setUpTestData():
        venue = Venue.objects.create(name="Venue 1", city="City", country="USA", altitude=100)
        team = Team.objects.create(name="Team 1", venue=venue)
        player = Player.objects.create(player_id="1", first_name="Lorem", last_name="Ipsum", dob="1999-12-31", current_team=team, height="100", weight="50", nationality="ESP")
        position = player.primary_positions.create(position_id="1", position="GK")
    #
	# The Player Edit view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('playersedit', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The Player Edit view should return the player_edit.html template
	# for rendering
	#
    def test_player_edit(self):
        response = self.client.get(reverse_lazy('playersedit', args=[1]))
        self.assertTemplateUsed(response=response, template_name='football/player_add.html', count=1)
    #
	# The Player Delete view should return a message if the player_id
	# does not belong to a player
	#
    def test_player_edit_404(self):
        response = self.client.get(reverse_lazy('playersedit', args=[55]))
        self.assertEquals(response.status_code, 404)
