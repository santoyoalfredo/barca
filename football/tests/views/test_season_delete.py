from django.test import TestCase
from django.urls import reverse_lazy

from football.models import *

class SeasonDeleteTests(TestCase):

    def setUpTestData():
        competition = Competition.objects.create(name="Test League", competition_format="l", promotion_limit="1", qualifying_limit="1", relegation_limit="1")
        venue = Venue.objects.create(name="Venue 1", city="City", country="USA", altitude=100)
        season = Season.objects.create(season_id="1", competition=competition, year=1999)
        team = season.teams.create(name="Team 1", venue=venue)
    #
	# The Season Delete view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('seasonsdelete', args=[1, 1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The Season Delete view should return the season_delete.html template
	# for rendering
	#
    def test_season_delete(self):
        response = self.client.get(reverse_lazy('seasonsdelete', args=[1, 1]))
        self.assertTemplateUsed(response=response, template_name='football/season_confirm_delete.html', count=1)
    #
	# The Season Delete view should display the name of the season
	# to be deleted
    def test_season_delete_name(self):
        response = self.client.get(reverse_lazy('seasonsdelete', args=[1, 1]))
        self.assertContains(response, "Test League 1999-2000")
    #
	# The Season Delete view should return a message if the season_id
	# does not belong to a competititon
	#
    def test_season_delete_404(self):
        response = self.client.get(reverse_lazy('seasonsdelete', args=[55, 55]))
        self.assertEquals(response.status_code, 404)
