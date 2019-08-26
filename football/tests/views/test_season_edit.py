from django.test import TestCase
from django.urls import reverse_lazy

from football.models import *

class SeasonEditTests(TestCase):

    def setUpTestData():
        competition = Competition.objects.create(name="Test League", competition_format="l", promotion_limit="1", qualifying_limit="1", relegation_limit="1")
        venue = Venue.objects.create(name="Venue 1", city="City", country="USA", altitude=100)
        season = Season.objects.create(season_id="1", competition=competition, year=1999)
        team = season.teams.create(name="Team 1", venue=venue)
    #
	# The Season Edit view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('seasonsedit', args=[1, 1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The Season Edit view should return the season_edit.html template
	# for rendering
	#
    def test_season_edit(self):
        response = self.client.get(reverse_lazy('seasonsedit', args=[1, 1]))
        self.assertTemplateUsed(response=response, template_name='football/season_add.html', count=1)
    #
	# The Season Edit view should return a message if the season_id
	# does not belong to a season
	#
    def test_season_edit_404(self):
        response = self.client.get(reverse_lazy('seasonsedit', args=[55, 55]))
        self.assertEquals(response.status_code, 404)
