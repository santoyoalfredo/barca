from django.test import TestCase
from unittest.mock import patch

from football.models import *

class CompetitionModelTests(TestCase):

    def test_save_blank_to_new_logo(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving a logo to an existing competition
        # without a logo
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            competition = Competition(name="Ipsum Lorem")
            competition.save()
            competition.logo = "lorem ipsum.png"
            competition.save()
            self.assertEqual(competition.logo, "competitions/Ipsum Lorem.png")
    
    def test_save_blank_logo(self):
        #
        # save() returns an empty string when saving a new competition without
        # a logo
        #
        competition = Competition(name="Ipsum Lorem")
        competition.save()
        self.assertEqual(competition.logo, "")

    def test_save_new_logo(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving a new competition with a logo
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            competition = Competition(name="Ipsum Lorem", logo="lorem ipsum.png")
            competition.save()
            self.assertEqual(competition.logo, "competitions/Ipsum Lorem.png")

    def test_save_old_name_to_new_name(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving an existing competition with a
        # different name
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            competition = Competition(name="Ipsum Lorem", logo="lorem ipsum.png")
            competition.save()
            competition.name = "Lorem Ipsum"
            competition.save()
            self.assertEqual(competition.logo, "competitions/Lorem Ipsum.png")

    def test_save_old_to_blank_logo(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving an existing competition and removing
        # its logo
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            competition = Competition(name="Ipsum Lorem", logo="lorem ipsum.png")
            competition.save()
            competition.logo = ""
            competition.save()
            self.assertEqual(competition.logo, "")
