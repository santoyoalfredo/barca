from django.test import TestCase
from unittest.mock import patch

from football.models import *

class PlayerModelTests(TestCase):

    def setUpTestData():
        venue = Venue.objects.create(name="ABC", city="ABC", country="ITA", altitude="50")
        Team.objects.create(team_id="1", name="LI", venue=venue)

    def test_save_blank_to_new_portrait(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving a portrait to an existing player
        # without a portrait
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            player = Player(player_id="20", first_name="Lorem", full_name="Lorem Ipsum", dob="1999-12-31", height="100", weight="50", current_team_id=1, nationality="ESP")
            player.save()
            player.portrait = "lorem ipsum.png"
            player.save()
            self.assertEqual(player.portrait.name, "players/%s/%s.png" % (player.nationality, player.player_id))
    
    def test_save_blank_portrait(self):
        #
        # save() returns an empty string when saving a new player without
        # a portrait
        #
        player = Player(player_id="20", first_name="Lorem", full_name="Lorem Ipsum", dob="1999-12-31", height="100", weight="50", current_team_id=1, nationality="ESP")
        player.save()
        self.assertEqual(player.portrait, "")

    def test_save_new_portrait(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving a new player with a portrait
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            player = Player(player_id="20", portrait="lorem ipsum.png", first_name="Lorem", full_name="Lorem Ipsum", dob="1999-12-31", height="100", weight="50", current_team_id=1, nationality="ESP")
            player.save()
            self.assertEqual(player.portrait.name, "players/%s/%s.png" % (player.nationality, player.player_id))

    def test_save_old_country_to_new_country(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving an existing player with a
        # different nationality
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            player = Player(player_id="20", portrait="lorem ipsum.png", first_name="Lorem", full_name="Lorem Ipsum", dob="1999-12-31", height="100", weight="50", current_team_id=1, nationality="ESP")
            player.save()
            player.nationality = "ITA"
            player.save()
            self.assertEqual(player.portrait.name, "players/%s/%s.png" % (player.nationality, player.player_id))

    def test_save_old_to_blank_portrait(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving an existing player and removing
        # its portrait
        #
            player = Player(player_id="20", first_name="Lorem", full_name="Lorem Ipsum", dob="1999-12-31", height="100", weight="50", current_team_id=1, nationality="ESP")
            player.save()
            player.portrait = ""
            player.save()
            self.assertEqual(player.portrait, "")
