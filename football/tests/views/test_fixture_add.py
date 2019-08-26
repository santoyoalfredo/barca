from django.test import TestCase
from django.urls import reverse_lazy

from football.forms import FixtureAddForm
from football.models import Competition, Season

class FixtureAddTests(TestCase):

    def setUpTestData():
        competition = Competition.objects.create(competition_id="1", name="Test League", competition_format="l", promotion_limit="1", qualifying_limit="1", relegation_limit="1")
        Season.objects.create(season_id="1", competition=competition, year=1999)
    #
	# The Fixture Add view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('fixturesadd', args=[1, 1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The Fixture Add view should return the fixture_add.html template
	# for rendering
	#
    def test_fixture_add(self):
        response = self.client.get(reverse_lazy('fixturesadd', args=[1, 1]))
        self.assertTemplateUsed(response=response, template_name='football/fixture_add.html', count=1)
    #
	# The Fixture Add view should display the correct form
	#
    def test_fixture_add_form(self):
        form = FixtureAddForm()
        self.assertTrue('season' in form.fields)
        self.assertTrue('home_team' in form.fields)
        self.assertTrue('away_team' in form.fields)
        self.assertTrue('home_score' in form.fields)
        self.assertTrue('away_score' in form.fields)
        self.assertTrue('location' in form.fields)
        self.assertTrue('date' in form.fields)
        self.assertTrue('time' in form.fields)
        self.assertTrue('weather' in form.fields)
        self.assertTrue('temperature' in form.fields)
        self.assertTrue('windchill' in form.fields)
        self.assertTrue('humidity' in form.fields)
        self.assertTrue('pressure' in form.fields)
        self.assertTrue('wind_direction' in form.fields)
        self.assertTrue('wind_speed' in form.fields)
        self.assertTrue('extra_time' in form.fields)
        self.assertTrue('penalty_shootout' in form.fields)
