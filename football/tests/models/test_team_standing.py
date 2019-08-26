from django.test import TestCase

from football.models import *

class TeamStandingTests(TestCase):

    def setUpTestData():
        venue = Venue.objects.create(name="ABC", city="ABC", country="ESP", altitude="50")
        team1 = Team.objects.create(team_id=1, venue=venue)
        team2 = Team.objects.create(team_id=2, venue=venue)
        competition = Competition.objects.create(name="COM")
        season = Season.objects.create(season_id=1, competition=competition, year=1999)
        fixture1 = Fixture.objects.create(fixture_id=1, season=season, home_team=team1, home_score=2, away_team=team2, extra_time=True, location=venue, date="1999-12-31", time="12:00")
        fixture2 = Fixture.objects.create(fixture_id=2, season=season, home_team=team2, home_score=2, away_team=team1, extra_time=True, location=venue, date="1999-12-31", time="12:00")

    def test_team_standing_creation(self):
        #
        # Fixture.save() creates a team standing object for each
        # team involved in the fixture
        #
        standing1 = TeamStanding.objects.get(team=1)
        standing2 = TeamStanding.objects.get(team=2)
        self.assertIsInstance(standing1, TeamStanding)
        self.assertIsInstance(standing2, TeamStanding)

    def test_team_standing_update(self):
        #
        #   On fixture deletion the post_delete signal should
        #   be received and relevant standings should update
        #
        Fixture.objects.get(fixture_id=1).delete()
        standing = TeamStanding.objects.get(team=1)
        self.assertEqual(1, standing.games_played)
        self.assertEqual(0, standing.wins)
        self.assertEqual(0, standing.overtime_wins)
        self.assertEqual(0, standing.goals_forced)
        self.assertEqual(-2, standing.goal_difference)
        self.assertEqual(0, standing.points)

    def testTeamStandingGamesPlayed(self):
        #
        # TeamStanding creation correctly calculates the number of
        # games played for a given team in a given season
        #
        standing = TeamStanding.objects.get(team=1, season=1)
        self.assertEqual(2, standing.games_played)

    def testTeamStandingWins(self):
        #
        # TeamStanding creation correctly calculates the number of
        # wins for a given team in a given season
        #
        standing = TeamStanding.objects.get(team=1, season=1)
        self.assertEqual(1, standing.wins)

    def testTeamStandingLosses(self):
        #
        # TeamStanding creation correctly calculates the number of
        # losses for a given team in a given season
        #
        standing = TeamStanding.objects.get(team=1, season=1)
        self.assertEqual(1, standing.losses)

    def testTeamStandingDraws(self):
        #
        # TeamStanding creation correctly calculates the number of
        # draws for a given team in a given season
        #
        standing = TeamStanding.objects.get(team=1, season=1)
        self.assertEqual(0, standing.draws)

    def testTeamStandingOvertimeWins(self):
        #
        # TeamStanding creation correctly calculates the number of
        # overtime wins for a given team in a given season
        #
        standing = TeamStanding.objects.get(team=1, season=1)
        self.assertEqual(1, standing.overtime_wins)

    def testTeamStandingOvertimeLosses(self):
        #
        # TeamStanding creation correctly calculates the number of
        # overtime losses for a given team in a given season
        #
        standing = TeamStanding.objects.get(team=1, season=1)
        self.assertEqual(1, standing.overtime_losses)

    def testTeamStandingGoalsForced(self):
        #
        # TeamStanding creation correctly calculates the number of
        # goals forced for a given team in a given season
        #
        standing = TeamStanding.objects.get(team=1, season=1)
        self.assertEqual(2, standing.goals_forced)

    def testTeamStandingGoalsAllowed(self):
        #
        # TeamStanding creation correctly calculates the number of
        # goals allowed for a given team in a given season
        #
        standing = TeamStanding.objects.get(team=1, season=1)
        self.assertEqual(2, standing.goals_allowed)

    def testTeamStandingGoalDifference(self):
        #
        # TeamStanding creation correctly calculates the goal
        # difference for a given team in a given season
        #
        standing = TeamStanding.objects.get(team=1, season=1)
        self.assertEqual(0, standing.goal_difference)

    def testTeamStandingPoints(self):
        #
        # TeamStanding creation correctly calculates the number of
        # points for a given team in a given season
        #
        standing = TeamStanding.objects.get(team=1, season=1)
        self.assertEqual(3, standing.points)
