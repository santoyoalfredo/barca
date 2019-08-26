from django.test import TestCase
from django.urls import reverse_lazy

from football.models import *

class FixtureEditTests(TestCase):

    def setUpTestData():
        competition = Competition.objects.create(name="Test League", competition_format="l", promotion_limit="1", qualifying_limit="1", relegation_limit="1")
        season = Season.objects.create(season_id="1", competition=competition, year=1999)
        venue = Venue.objects.create(name="ABC", city="ABC", country="ITA", altitude="50")
        team1 = Team.objects.create(team_id="1", name="LI", venue=venue)
        team2 = Team.objects.create(team_id="2", name="IL", venue=venue)
        fixture = Fixture.objects.create(fixture_id=1, season=season, home_team=team1, away_team=team2, home_score=1, away_score=1, location=venue, date="1999-01-01", time="12:00:00")
    #
	# The Fixture Edit view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('fixturesedit', args=[1, 1, 1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The Fixture Edit view should return the fixture_edit.html template
	# for rendering
	#
    def test_fixture_edit(self):
        response = self.client.get(reverse_lazy('fixturesedit', args=[1, 1, 1]))
        self.assertTemplateUsed(response=response, template_name='football/fixture_add.html', count=1)
    #
	# The Fixture Edit view should return a message if the fixture_id
	# does not belong to a fixture
	#
    def test_fixture_edit_404(self):
        response = self.client.get(reverse_lazy('fixturesedit', args=[55, 55, 55]))
        self.assertEquals(response.status_code, 404)
