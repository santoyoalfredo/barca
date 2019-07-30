from django.test import TestCase
from django.urls import reverse_lazy

from football.forms import SeasonAddForm
from football.models import Competition

class SeasonAddTests(TestCase):

    def setUpTestData():
        Competition.objects.create(competition_id="1", name="Test League", competition_format="l", promotion_limit="1", qualifying_limit="1", relegation_limit="1")
    #
	# The Season Add view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('seasonsadd', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The Season Add view should return the season_add.html template
	# for rendering
	#
    def test_season_add(self):
        response = self.client.get(reverse_lazy('seasonsadd', args=[1]))
        self.assertTemplateUsed(response=response, template_name='football/season_add.html', count=1)
    #
	# The Season Add view should display the correct form
	#
    def test_season_add_form(self):
        form = SeasonAddForm()
        self.assertTrue('competition' in form.fields)
        self.assertTrue('year' in form.fields)
        self.assertTrue('teams' in form.fields)
