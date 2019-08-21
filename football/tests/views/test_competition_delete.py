from django.test import TestCase
from django.urls import reverse_lazy

from football.models import *

class CompetitionDeleteTests(TestCase):

    def setUpTestData():
        Competition.objects.create(competition_id="1", name="Test League", competition_format="l", promotion_limit="1", qualifying_limit="1", relegation_limit="1")
    #
	# The Competition Delete view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('competitionsdelete', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The Competition Delete view should return the competition_delete.html template
	# for rendering
	#
    def test_competition_delete(self):
        response = self.client.get(reverse_lazy('competitionsdelete', args=[1]))
        self.assertTemplateUsed(response=response, template_name='football/competition_confirm_delete.html', count=1)
    #
	# The Competition Delete view should display the name of the competition
	# to be deleted
    def test_competition_delete_name(self):
        response = self.client.get(reverse_lazy('competitionsdelete', args=[1]))
        self.assertContains(response, "Test League")
    #
	# The Competition Delete view should return a message if the competititon_id
	# does not belong to a competititon
	#
    def test_competititon_delete_404(self):
        response = self.client.get(reverse_lazy('competitionsdelete', args=[55]))
        self.assertEquals(response.status_code, 404)
