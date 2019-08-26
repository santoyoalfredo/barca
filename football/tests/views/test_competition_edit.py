from django.test import TestCase
from django.urls import reverse_lazy
from unittest.mock import patch

from football.models import Competition

class CompetitionEditTests(TestCase):

    def setUpTestData():
        with patch('os.replace') as MockClass:
            Competition.objects.create(competition_id="1", name="Test League", logo="logo.png",competition_format="l", promotion_limit="1", qualifying_limit="1", relegation_limit="1")
    #
	# The Competition Edit view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('competitionsedit', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The Competition Edit view should return the competition_edit.html template
	# for rendering
	#
    def test_competition_edit(self):
        response = self.client.get(reverse_lazy('competitionsedit', args=[1]))
        self.assertTemplateUsed(response=response, template_name='football/competition_add.html', count=1)
    #
	# The Competition Delete view should return a message if the competititon_id
	# does not belong to a competititon
	#
    def test_competititon_edit_404(self):
        response = self.client.get(reverse_lazy('competitionsedit', args=[55]))
        self.assertEquals(response.status_code, 404)
