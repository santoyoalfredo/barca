from django.test import TestCase
from unittest.mock import patch

from football.models import *

class FixtureModelTests(TestCase):

    def setUpTestData():
        with patch('football.models.TeamStanding') as MockClass:
            instance = MockClass.return_value
            venue1 = Venue.objects.create(venue_id=1, name="ABC", city="ABC", country="ESP", altitude="50")
            venue2 = Venue.objects.create(venue_id=2, name="XYZ", city="XYZ", country="ESP", altitude="50")
            team1 = Team.objects.create(venue=venue1)
            team2 = Team.objects.create(venue=venue2)
            competition = Competition.objects.create(name="COM")
            season = Season.objects.create(competition=competition, year=1999)
            Fixture.objects.create(fixture_id=1, season=season, home_team=team1, away_team=team2, date="1999-12-31", time="12:00")
            Fixture.objects.create(fixture_id=2, season=season, home_team=team1, away_team=team2, location=venue2, date="1999-12-31", time="12:00")

    def test_save_location_if_empty(self):
        #
        # save() sets the venue of the home team if the location is
        # not provided when creating a new fixture
        #
        venue = Venue.objects.get(pk=1)
        fixture = Fixture.objects.get(pk=1)
        self.assertEqual(fixture.location, venue)
    
    def test_save_location_if_removed(self):
        #
        # save() sets the venue of the home team if the location is
        # removed from an existing fixture
        #
        venue = Venue.objects.get(pk=1)
        fixture = Fixture.objects.get(pk=2)
        fixture.location = None
        fixture.save()         
        self.assertEqual(fixture.location, venue)
