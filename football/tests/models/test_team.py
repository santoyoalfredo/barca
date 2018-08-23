from django.test import TestCase
from unittest.mock import patch

from football.models import *

class TeamModelTests(TestCase):

    def test_save_blank_to_new_crest(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving a crest to an existing team
        # without a crest
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            venue = Venue(name="ABC", city="ABC", country="ITA", altitude="50")
            venue.save()
            team = Team(team_id="1", name="LI", venue=venue)
            team.save()
            team.crest = "lorem ipsum.png"
            team.save()
            self.assertEqual(team.crest, "teams/%s/%s.png" % (venue.country, team.team_id))
    
    def test_save_blank_crest(self):
        #
        # save() returns an empty string when saving a new team without
        # a crest
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            venue = Venue(name="ABC", city="ABC", country="ITA", altitude="50")
            venue.save()
            team = Team(team_id="1", name="LI", venue=venue)
            team.save()
            self.assertEqual(team.crest, "")

    def test_save_new_crest(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving a new team with a crest
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            venue = Venue(name="ABC", city="ABC", country="ITA", altitude="50")
            venue.save()
            team = Team(team_id="1", name="LI", venue=venue, crest="lorem ipsum.png")
            team.save()
            self.assertEqual(team.crest, "teams/%s/%s.png" % (venue.country, team.team_id))

    def test_save_old_country_to_new_country(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving an existing team with a
        # different country
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            venue = Venue(name="ABC", city="ABC", country="ITA", altitude="50")
            venue.save()
            team = Team(team_id="1", name="LI", venue=venue, crest="lorem ipsum.png")
            team.save()
            venue.country = "FRA"
            venue.save()
            team.save()
            self.assertEqual(team.crest, "teams/%s/%s.png" % (venue.country, team.team_id))

    def test_save_old_to_blank_crest(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving an existing player and removing
        # its portrait
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            venue = Venue(name="ABC", city="ABC", country="ITA", altitude="50")
            venue.save()
            team = Team(team_id="1", name="LI", venue=venue, crest="lorem ipsum.png")
            team.save()
            team.crest = ""
            team.save()
            self.assertEqual(team.crest, "")
