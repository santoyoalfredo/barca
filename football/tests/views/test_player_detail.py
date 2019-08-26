from django.test import TestCase
from django.urls import reverse_lazy
from unittest.mock import patch

from football.models import *

class PlayerDetailViewTests(TestCase):

    def setUpTestData():
        venue = Venue.objects.create(name="ABC", city="ABC", country="ITA", altitude="50")
        Team.objects.create(team_id="1", name="LI", venue=venue)
        Position.objects.create(position_id="1", position="GK")
        Position.objects.create(position_id="2", position="CB")
    #
	# The PlayerDetail view should return the base.html template
	# for rendering
	#
    def test_base(self):
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            Player.objects.create(player_id="20", portrait="lorem ipsum.png", first_name="Lorem", full_name="Lorem Ipsum", dob="1999-12-31", height="100", weight="50", current_team_id=1, nationality="ESP")
            response = self.client.get(reverse_lazy('player', args=[20]))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The PlayerDetail view should return the player_detail.html template
	# for rendering
	#
    def test_player_detail(self):
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            Player.objects.create(player_id="20", portrait="lorem ipsum.png", first_name="Lorem", full_name="Lorem Ipsum", dob="1999-12-31", height="100", weight="50", current_team_id=1, nationality="ESP")
            response = self.client.get(reverse_lazy('player', args=[20]))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response=response, template_name='football/player_detail.html', count=1)
    #
	# The PlayerDetail view should return a message if the player_id
	# does not belong to a player
	#
    def test_player_404(self):
        response = self.client.get(reverse_lazy('player', args=[55]))
        self.assertEquals(response.status_code, 404)
    #
	# The PlayerDetail view should return a player if it exists
    # and display its information
	#
    def test_player_info(self):
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            player = Player(player_id="20", portrait="lorem ipsum.png", first_name="Lorem", full_name="Lorem Ipsum", dob="1999-12-31", height="100", weight="50", current_team_id=1, nationality="ESP")
            player.primary_positions.set([1])
            player.secondary_positions.set([2])
            player.save()
            response = self.client.get(reverse_lazy('player', args=[20]))
            self.assertContains(response, "Lorem Ipsum")
            self.assertContains(response, "players/ESP/20.png")
            self.assertContains(response, "ESP.svg")
            self.assertContains(response, "100 cm")
            self.assertContains(response, "3'3")
            self.assertContains(response, "50 Kg")
            self.assertContains(response, "110 lbs")
            self.assertQuerysetEqual(response.context['player'].primary_positions.all(), ['<Position: GK>'])
            self.assertQuerysetEqual(response.context['player'].secondary_positions.all(), ['<Position: CB>'])
    #
	# The PlayerDetail template should provide a fallback portrait
    # if a player has none
	#
    def test_player_without_portrait(self):
        Player.objects.create(player_id="20", first_name="Lorem", full_name="Lorem Ipsum", dob="1999-12-31", height="100", weight="50", current_team_id=1, nationality="ESP")
        response = self.client.get(reverse_lazy('player', args=[20]))
        self.assertEquals(response.context['player'].portrait, '')
        self.assertContains(response, "player.svg")
    #
	# The PlayerDetail template should provide a fallback team crest
    # if a player's current team has no crest
	#
    def test_player_without_current_team(self):
        Player.objects.create(player_id="20", first_name="Lorem", full_name="Lorem Ipsum", dob="1999-12-31", height="100", weight="50", current_team_id=1, nationality="ESP")
        response = self.client.get(reverse_lazy('player', args=[20]))
        self.assertEquals(response.context['player'].current_team.crest, '')
        self.assertContains(response, "team.svg")
