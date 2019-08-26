from django.test import TestCase
from django.urls import reverse_lazy
from unittest.mock import patch

from football.models import *

def create_player(first_name, last_name, nationality, portrait, current_team):
    with patch('os.replace') as MockClass:
        instance = MockClass.return_value
        if(current_team):
            venue = Venue.objects.create(name="ABC", city="ABC", country="ITA", altitude="50")
            team = Team.objects.create(team_id=current_team, name="LI", venue=venue)
            return Player.objects.create(first_name=first_name, last_name=last_name, full_name="%s %s" % (first_name, last_name), nationality=nationality, dob="1999-12-31", height="100", weight="50", portrait=portrait, current_team=team)
        else:
            player = Player(first_name=first_name, last_name=last_name, full_name="%s %s" % (first_name, last_name), nationality=nationality, dob="1999-12-31", height="100", weight="50", portrait=portrait)
            return player

class PlayerListViewTests(TestCase):
    #
	# The PlayerList view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('players'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The PlayerList view should return the player_list.html template
	# for rendering
	#
    def test_player_list(self):
        response = self.client.get(reverse_lazy('players'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/player_list.html', count=1)
    #
	# The PlayerList view should return a message if there are no
	# players
	#
    def test_no_players(self):
        response = self.client.get(reverse_lazy('players'))
        self.assertContains(response, "There are no players")
        self.assertQuerysetEqual(response.context['players'], [])
    #
	# The PlayerList view should return a player if it exists
    # and display its information
	#
    def test_player(self):
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            player = create_player("Lorem", "Ipsum", "ESP", "image.png", 1)
            player.save()
            response = self.client.get(reverse_lazy('players'))
            self.assertQuerysetEqual(response.context['players'], ['<Player: Lorem Ipsum>'])
            self.assertContains(response, "Lorem Ipsum")
            self.assertContains(response, player.portrait.name)
            self.assertContains(response, "ESP.svg")
    #
	# The PlayerList view should return a list of players if
    # multiple exist and display respective information
	#
    def test_players(self):
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            player1 = create_player("Lorem", "Ipsum", "ESP", "image.png", 1)
            player2 = create_player("Ipsum", "Lorem", "ITA", "image.png", 2)
            player1.save()
            player2.save()
            response = self.client.get(reverse_lazy('players'))
            self.assertQuerysetEqual(response.context['players'], ['<Player: Lorem Ipsum>', '<Player: Ipsum Lorem>'])
            self.assertContains(response, "Lorem Ipsum")
            self.assertContains(response, player1.portrait.name)
            self.assertContains(response, "ESP.svg")
            self.assertContains(response, "Ipsum Lorem")
            self.assertContains(response, player2.portrait.name)
            self.assertContains(response, "ITA.svg")
    #
	# The PlayerList template should provide a fallback portrait
    # if a player has none
	#
    def test_player_without_portrait(self):
        create_player("Lorem", "Ipsum", "ESP", "", 1)
        response = self.client.get(reverse_lazy('players'))
        self.assertEquals(response.context['players'][0].portrait, '')
        self.assertContains(response, "player.svg")
    #
	# The PlayerList template should provide a fallback team crest
    # if a player's current team has no crest
	#
    def test_player_without_current_team(self):
        create_player("Lorem", "Ipsum", "ESP", "image.png", 1)
        response = self.client.get(reverse_lazy('players'))
        self.assertEquals(response.context['players'][0].current_team.crest, '')
        self.assertContains(response, "team.svg")
