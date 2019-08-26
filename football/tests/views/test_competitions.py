from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy
from unittest.mock import patch

from football.models import *

class CompetitionsViewTests(TestCase):

    def setUpTestData():
        User.objects.create_user(username="user", password="password", is_staff=True)
    #
	# The Competitions view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('competitions'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The Competitions view should return the competitions.html template
	# for rendering
	#
    def test_competitions(self):
        response = self.client.get(reverse_lazy('competitions'))
        self.assertTemplateUsed(response=response, template_name='football/competitions.html', count=1)
    #
	# The Competitions view should return a message if there are no
	# competitions
	#
    def test_no_competitions(self):
        response = self.client.get(reverse_lazy('competitions'))
        self.assertContains(response, "There are no competitions")
        self.assertQuerysetEqual(response.context['competitions'], [])
    #
	# The Competitions view should return a competition if it exists
    # and display its information
	#
    def test_competition(self):
        with patch('os.replace') as MockClass:
            competition = Competition(name="League", logo="logo.png", competition_format="l", promotion_limit=1, qualifying_limit=2, relegation_limit=1)
            competition.save()
            response = self.client.get(reverse_lazy('competitions'))
            self.assertQuerysetEqual(response.context['competitions'], ['<Competition: League>'])
            self.assertContains(response, "League")
            self.assertContains(response, competition.logo.name)
    #
	# The Competitions view should return a list of competitions if
    # multiple exist and display respective information
	#
    def test_competitions_list(self):
        with patch('os.replace') as MockClass:
            competition1 = Competition(name="League", logo="logo.png", competition_format="l", promotion_limit=1, qualifying_limit=2, relegation_limit=1)
            competition2 = Competition(name="Cup", logo="logo.png", competition_format="k", promotion_limit=0, qualifying_limit=0, relegation_limit=0)
            competition1.save()
            competition2.save()
            response = self.client.get(reverse_lazy('competitions'))
            self.assertQuerysetEqual(response.context['competitions'], ['<Competition: Cup>', '<Competition: League>'])
            self.assertContains(response, "League")
            self.assertContains(response, competition1.logo.name)
            self.assertContains(response, "Cup")
            self.assertContains(response, competition2.logo.name)
    #
	# The Competitions template should provide a fallback logo
    # if a competition has none
	#
    def test_competition_without_logo(self):
        competition = Competition(name="League", competition_format="l", promotion_limit=1, qualifying_limit=2, relegation_limit=1)
        competition.save()
        response = self.client.get(reverse_lazy('competitions'))
        self.assertEquals(response.context['competitions'][0].logo, '')
        self.assertContains(response, "competition.svg")
    #
	# The Competitions template should provide a default message
    # if a competition has no seasons
	#
    def test_competition_without_seasons(self):
        competition = Competition(name="League", competition_format="l", promotion_limit=1, qualifying_limit=2, relegation_limit=1)
        competition.save()
        self.client.login(username="user", password="password")
        response = self.client.get(reverse_lazy('competitions'))
        self.assertQuerysetEqual(response.context['competitions'], ['<Competition: League>'])
        self.assertContains(response, "League")
        self.assertContains(response, "Add a Season")
    #
	# The Competitions template should provide a list of seasons
    # if a competition has at least one season
	#
    def test_competition_with_seasons(self):
        competition = Competition(name="League", competition_format="l", promotion_limit=1, qualifying_limit=2, relegation_limit=1)
        competition.save()
        season = Season(competition=competition, year=2000)
        season.save()
        response = self.client.get(reverse_lazy('competitions'))
        self.assertQuerysetEqual(response.context['competitions'], ['<Competition: League>'])
        self.assertContains(response, "League")
        self.assertContains(response, "2000")
