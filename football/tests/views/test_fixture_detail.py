from django.test import TestCase
from django.urls import reverse_lazy
from unittest.mock import patch

from football.models import *

class FixtureDetailViewTests(TestCase):
    def setUpTestData():
        with patch('os.replace') as MockClass:
            venue1 = Venue.objects.create(venue_id=1, name="ABC", city="ABC", country="ITA", altitude="50", picture="picture.jpg")
            venue2 = Venue.objects.create(venue_id=2, name="ABC", city="ABC", country="ITA", altitude="50")
            team1 = Team.objects.create(team_id=1, name="LI", venue=venue1, crest="crest.png")
            team2 = Team.objects.create(team_id=2, name="IL", venue=venue2)
            competition = Competition.objects.create(competition_id=1, name="League", competition_format="l")
            season = Season.objects.create(season_id=20, competition=competition, year=2000)
            fixture1 = Fixture.objects.create(fixture_id=55, season=season, home_team=team1, away_team=team2, date='2000-01-01', time='12:00:00', home_score=2, away_score=1)
            fixture2 = Fixture.objects.create(fixture_id=56, season=season, home_team=team2, away_team=team1, date='2000-01-01', time='12:00:00', home_score=2, away_score=1)
            player1 = Player.objects.create(first_name='Lorem', last_name='Ipsum', full_name='Lorem Ipsum', nationality='ESP', dob="1999-12-31", height="100", weight="50", current_team=team1)
            player2 = Player.objects.create(first_name='New', last_name='Player', full_name='New Player', nationality='ESP', dob="1999-12-31", height="100", weight="50", current_team=team1)
            FixtureEvent.objects.create(event_type='G', fixture=fixture1, team=team1, player=player1, period='1', minute=47)
            FixtureEvent.objects.create(event_type='G', fixture=fixture1, team=team1, player=player1, period='1', minute=35)
            FixtureEvent.objects.create(event_type='P', fixture=fixture1, team=team1, player=player2, period='2', minute=95)
            FixtureEvent.objects.create(event_type='P', fixture=fixture1, team=team1, player=player2, period='2', minute=90)
            FixtureEvent.objects.create(event_type='O', fixture=fixture1, team=team1, player=player1, period='1', minute=30)
            FixtureEvent.objects.create(event_type='R', fixture=fixture1, team=team1, player=player1, period='2', minute=69)
            Statistics.objects.create(fixture_id=fixture1, player_id=player1, goals=1, assists=2, shots=5)

    #
	# The FixtureDetail view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The FixtureDetail view should return the fixture_detail.html template
	# for rendering
	#
    def test_fixture_detail(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        self.assertTemplateUsed(response=response, template_name='football/fixture_detail.html', count=1)

    #
	# The FixtureDetail view should display the appropriate information for
	# the home team
	#
    def test_fixture_detail_home_team(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        self.assertEquals(response.context['fixture'].home_team.name, "LI")
        self.assertEquals(response.context['fixture'].home_team.crest, "teams/ITA/1.png")
    
    #
	# The FixtureDetail view should display the appropriate information for
	# the away team
	#
    def test_fixture_detail_away_team(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        self.assertEquals(response.context['fixture'].away_team.name, "IL")
        self.assertContains(response, "team.svg")

    #
	# The FixtureDetail view should display the appropriate information for
	# the fixture
	#
    def test_fixture_detail_info(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        self.assertEquals(response.context['fixture'].home_score, 2)
        self.assertEquals(response.context['fixture'].away_score, 1)
        self.assertEquals(response.context['fixture'].location.name, "ABC")
        self.assertContains(response, "Saturday January 01, 2000")
        self.assertContains(response, "12:00")
    
    #
	# The FixtureDetail view should display the appropriate venue image for
	# the location of the fixture
	#
    def test_fixture_detail_venue_image(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        self.assertContains(response, "venues/ITA/1.jpg")

    #
	# The FixtureDetail view should display the fallback venue image when
	# there isn't one available
	#
    def test_fixture_detail_venue_image(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,56]))
        self.assertContains(response, "stadium.jpg")

    #
	# The FixtureDetail view should display the appropriate information for
	# a goal event
	#
    def test_fixture_detail_goal_event(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        self.assertEqual(["35'", "45+2'"], response.context['homeEvents']['Lorem Ipsum'])

    #
	# The FixtureDetail view should display the appropriate information for
	# an own goal event
    #
    def test_fixture_detail_own_goal_event(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        self.assertEqual(["30' (OG)"], response.context['awayEvents']['Lorem Ipsum'])

    #
	# The FixtureDetail view should display the appropriate information for
	# a penalty event
    #
    def test_fixture_detail_penalty_event(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        self.assertEqual(["90' (P)", "90+5' (P)"], response.context['homeEvents']['New Player'])
    
    #
	# The FixtureDetail view should display the appropriate information for
	# a red card event
    #
    def test_fixture_detail_red_card_event(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        self.assertEqual("69'", response.context['homeRedEvents']['Lorem Ipsum'])

    #
	# The FixtureDetail view should display the appropriate information for
	# an event that occurred during extra time
    #
    def test_fixture_detail_extra_time_event(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        self.assertEqual(["90' (P)", "90+5' (P)"], response.context['homeEvents']['New Player'])

    #
	# The FixtureDetail view should display the appropriate information for
	# multiple events of a single player
    #
    def test_fixture_detail_player_events(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        self.assertEqual(["35'", "45+2'"], response.context['homeEvents']['Lorem Ipsum'])

    #
	# The FixtureDetail view should display the appropriate information for
	# multiple events in chronological order
    #
    def test_fixture_detail_chronologial_events(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        self.assertEqual(["35'", "45+2'"], response.context['homeEvents']['Lorem Ipsum'])
        self.assertEqual(["90' (P)", "90+5' (P)"], response.context['homeEvents']['New Player'])
    
    #
	# The FixtureDetail view should display the appropriate information for
	# player statistics
    #
    def test_fixture_detail_player_statistics(self):
        response = self.client.get(reverse_lazy('fixture', args=[1,20,55]))
        stats = Statistics.objects.filter(fixture_id=55)
        self.assertEqual('Lorem Ipsum', stats[0].player_id.get_name())
        self.assertEqual(1, stats[0].goals)
        self.assertEqual(2, stats[0].assists)
        self.assertEqual(5, stats[0].shots)
