from django.test import TestCase
from django.urls import reverse_lazy
from unittest.mock import patch

from football.models import *

class SeasonDetailViewTests(TestCase):

    def setUpTestData():
        with patch('os.replace') as MockClass:
            venue = Venue.objects.create(name="ABC", city="ABC", country="ITA", altitude="50")
            Team.objects.create(team_id="1", name="LI", venue=venue)
            Team.objects.create(team_id="2", name="IL", venue=venue)
    #
	# The SeasonDetail view should return the base.html template
	# for rendering
	#
    def test_base(self):
        with patch('os.replace') as MockClass:
            competition = Competition(competition_id=1, name="League", logo="league logo.png", competition_format="l", promotion_limit=1, qualifying_limit=2, relegation_limit=1)
            competition.save()
            season = Season(season_id="20", competition=competition, year=2000)
            season.teams.set([1])
            season.save()
            response = self.client.get(reverse_lazy('season', args=[1,20]))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The SeasonDetail view should return the season_detail.html template
	# for rendering
	#
    def test_season_detail(self):
        with patch('os.replace') as MockClass:
            competition = Competition(competition_id=1, name="League", logo="league logo.png", competition_format="l", promotion_limit=1, qualifying_limit=2, relegation_limit=1)
            competition.save()
            season = Season(season_id="20", competition=competition, year=2000)
            season.teams.set([1])
            season.save()
            response = self.client.get(reverse_lazy('season', args=[1,20]))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response=response, template_name='football/season_detail.html', count=1)
    #
	# The SeasonDetail view should display the competition logo for the
	# respective season
	#
    def test_season_detail_logo(self):
        with patch('os.replace') as MockClass:
            competition = Competition(competition_id=1, name="League", logo="league logo.png", competition_format="l", promotion_limit=1, qualifying_limit=2, relegation_limit=1)
            competition.save()
            season = Season(season_id="20", competition=competition, year=2000)
            season.teams.set([1])
            season.save()
            response = self.client.get(reverse_lazy('season', args=[1,20]))
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, "competitions/League.png")
    #
	# The SeasonDetail view should display a fallback competition logo for the
	# respective season
	#
    def test_season_detail_without_logo(self):
        with patch('os.replace') as MockClass:
            competition = Competition(competition_id=1, name="League", competition_format="l", promotion_limit=1, qualifying_limit=2, relegation_limit=1)
            competition.save()
            season = Season(season_id="20", competition=competition, year=2000)
            season.teams.set([1])
            season.save()
            response = self.client.get(reverse_lazy('season', args=[1,20]))
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, "competition.svg")
    #
	# The SeasonDetail view should display the competition standings for the
	# respective season
	#
    def test_season_detail(self):
        competition = Competition.objects.create(competition_id=1, name="League", competition_format="l")
        venue = Venue.objects.create(name="ABC", city="ABC", country="ITA", altitude=50)
        team1 = Team.objects.create(team_id=3, name="LI", venue=venue)
        team2 = Team.objects.create(team_id=4, name="IL", venue=venue)
        season = Season.objects.create(season_id=20, competition=competition, year=2000)
        fixture = Fixture.objects.create(season=season, home_team=team1, away_team=team2, date='2000-01-01', time='12:00:00', home_score=5, away_score=1)
        response = self.client.get(reverse_lazy('season', args=[1,20]))
        self.assertEquals(response.status_code, 200)
        self.assertInHTML('''<tr >
                                    <td>1</td>
                                    <td class="align-middle"><img src="/resources/" class="img-portrait-sm mx-auto d-block"></td>
                                    <td>LI</td>
                                    <td>1</td>
                                    <td>1</td>
                                    <td>0</td>
                                    <td>0</td>
                                    <td>5</td>
                                    <td>1</td>
                                    <td>4</td>
                                    <td>3</td>
                                </tr>''', response.content.decode())
    #
	# The SeasonDetail view should highlight the promoted teams in the standings for
	# respective season
	#
    def test_season_detail_promotion(self):
        competition = Competition.objects.create(competition_id=1, name="League", competition_format="l", promotion_limit=1)
        venue = Venue.objects.create(name="ABC", city="ABC", country="ITA", altitude=50)
        team1 = Team.objects.create(team_id=3, name="LI", venue=venue)
        team2 = Team.objects.create(team_id=4, name="IL", venue=venue)
        season = Season.objects.create(season_id=20, competition=competition, year=2000)
        fixture = Fixture.objects.create(season=season, home_team=team1, away_team=team2, date='2000-01-01', time='12:00:00', home_score=5, away_score=1)
        response = self.client.get(reverse_lazy('season', args=[1,20]))
        self.assertEquals(response.status_code, 200)
        self.assertInHTML('''<tr class="table-success">
                                    <td>1</td>
                                    <td class="align-middle"><img src="/resources/" class="img-portrait-sm mx-auto d-block"></td>
                                    <td>LI</td>
                                    <td>1</td>
                                    <td>1</td>
                                    <td>0</td>
                                    <td>0</td>
                                    <td>5</td>
                                    <td>1</td>
                                    <td>4</td>
                                    <td>3</td>
                                </tr>''', response.content.decode())
    #
	# The SeasonDetail view should highlight the qualifying teams in the standings for
	# respective season
	#
    def test_season_detail_qualifying(self):
        competition = Competition.objects.create(competition_id=1, name="League", competition_format="l", qualifying_limit=1)
        venue = Venue.objects.create(name="ABC", city="ABC", country="ITA", altitude=50)
        team1 = Team.objects.create(team_id=3, name="LI", venue=venue)
        team2 = Team.objects.create(team_id=4, name="IL", venue=venue)
        season = Season.objects.create(season_id=20, competition=competition, year=2000)
        fixture = Fixture.objects.create(season=season, home_team=team1, away_team=team2, date='2000-01-01', time='12:00:00', home_score=5, away_score=1)
        response = self.client.get(reverse_lazy('season', args=[1,20]))
        self.assertEquals(response.status_code, 200)
        self.assertInHTML('''<tr class="table-warning">
                                    <td>1</td>
                                    <td class="align-middle"><img src="/resources/" class="img-portrait-sm mx-auto d-block"></td>
                                    <td>LI</td>
                                    <td>1</td>
                                    <td>1</td>
                                    <td>0</td>
                                    <td>0</td>
                                    <td>5</td>
                                    <td>1</td>
                                    <td>4</td>
                                    <td>3</td>
                                </tr>''', response.content.decode())
    #
	# The SeasonDetail view should highlight the relegated teams in the standings for
	# respective season
	#
    def test_season_detail_relegation(self):
        competition = Competition.objects.create(competition_id=1, name="League", competition_format="l", relegation_limit=1)
        venue = Venue.objects.create(name="ABC", city="ABC", country="ITA", altitude=50)
        team1 = Team.objects.create(team_id=3, name="LI", venue=venue)
        team2 = Team.objects.create(team_id=4, name="IL", venue=venue)
        season = Season.objects.create(season_id=20, competition=competition, year=2000)
        fixture = Fixture.objects.create(season=season, home_team=team1, away_team=team2, date='2000-01-01', time='12:00:00', home_score=5, away_score=1)
        response = self.client.get(reverse_lazy('season', args=[1,20]))
        self.assertEquals(response.status_code, 200)
        self.assertInHTML('''<tr class="table-danger">
                                    <td>2</td>
                                    <td class="align-middle"><img src="/resources/" class="img-portrait-sm mx-auto d-block"></td>
                                    <td>IL</td>
                                    <td>1</td>
                                    <td>0</td>
                                    <td>0</td>
                                    <td>1</td>
                                    <td>1</td>
                                    <td>5</td>
                                    <td>-4</td>
                                    <td>0</td>
                                </tr>''', response.content.decode())
    #
	# The SeasonDetail view should display the competition fixtures for the
	# respective season
	#
    def test_season_detail_fixtures(self):
        competition = Competition.objects.create(competition_id=1, name="League", competition_format="l", promotion_limit=1)
        venue = Venue.objects.create(name="ABC", city="ABC", country="ITA", altitude=50)
        team1 = Team.objects.create(team_id=3, name="LI", venue=venue)
        team2 = Team.objects.create(team_id=4, name="IL", venue=venue)
        season = Season.objects.create(season_id=20, competition=competition, year=2000)
        fixture = Fixture.objects.create(fixture_id=55, season=season, home_team=team1, away_team=team2, date='2000-01-01', time='12:00:00', home_score=5, away_score=1)
        response = self.client.get(reverse_lazy('season', args=[1,20]))
        self.assertEquals(response.status_code, 200)
        self.assertInHTML('''<tr>
                                    <td>01-01-2000</td>
                                    <td>LI</td>
                                    <td>5</td>
                                    <td>-</td>
                                    <td>1</td>
                                    <td>IL</td>
                                    <td><a href="/competitions/1/20/55" role="button" class="btn btn-primary">Match Info</a></td>
                                </tr>''', response.content.decode())
    #
	# The SeasonDetail view should return a message if the season_id
	# does not belong to a season
	#
    def test_season_404(self):
        response = self.client.get(reverse_lazy('season', args=[55]))
        self.assertEquals(response.status_code, 404)
