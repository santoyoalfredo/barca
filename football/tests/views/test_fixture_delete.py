from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from football.models import *

class FixtureDeleteTests(TestCase):

    def setUpTestData():
        User.objects.create_user(username="user", password="password", is_staff=True)
        competition = Competition.objects.create(name="Test League", competition_format="l", promotion_limit="1", qualifying_limit="1", relegation_limit="1")
        season = Season.objects.create(season_id="1", competition=competition, year=1999)
        venue = Venue.objects.create(name="ABC", city="ABC", country="ITA", altitude="50")
        team1 = Team.objects.create(team_id="1", name="LI", venue=venue)
        team2 = Team.objects.create(team_id="2", name="IL", venue=venue)
        fixture = Fixture.objects.create(fixture_id=1, season=season, home_team=team1, away_team=team2, home_score=1, away_score=1, location=venue, date="1999-01-01", time="12:00:00")
    #
	# The Fixture Delete view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('fixturesdelete', args=[1, 1, 1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The Fixture Delete view should return the fixture_delete.html template
	# for rendering
	#
    def test_fixture_delete(self):
        response = self.client.get(reverse_lazy('fixturesdelete', args=[1, 1, 1]))
        self.assertTemplateUsed(response=response, template_name='football/fixture_confirm_delete.html', count=1)
    #
	# The Fixture Delete view should display the name of the fixture
	# to be deleted
    def test_season_delete_name(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse_lazy('fixturesdelete', args=[1, 1, 1]))
        self.assertContains(response, "1999-01-01 - LI 1-1 IL")
    #
	# The Fixture Delete view should return a message if the fixture_id
	# does not belong to a season
	#
    def test_season_delete_404(self):
        response = self.client.get(reverse_lazy('fixturesdelete', args=[55, 55, 55]))
        self.assertEquals(response.status_code, 404)
