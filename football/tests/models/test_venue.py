from django.test import TestCase
from unittest.mock import patch

from football.models import *

class VenueModelTests(TestCase):

    def test_save_blank_to_new_picture(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving a picture to an existing venue
        # without a picture
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            venue = Venue(venue_id="1", name="ABC", city="ABC", country="ITA", altitude="50")
            venue.save()
            venue.picture = "lorem ipsum.png"
            venue.save()
            self.assertEqual(venue.picture, "venues/%s/%s.png" % (venue.country, venue.venue_id))
    
    def test_save_blank_picture(self):
        #
        # save() returns an empty string when saving a new venue without
        # a picture
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            venue = Venue(name="ABC", city="ABC", country="ITA", altitude="50")
            venue.save()
            self.assertEqual(venue.picture, "")

    def test_save_new_picture(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving a new venue with a picture
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            venue = Venue(venue_id="1", name="ABC", city="ABC", country="ITA", altitude="50", picture="lorem ipsum.png")
            venue.save()
            self.assertEqual(venue.picture, "venues/%s/%s.png" % (venue.country, venue.venue_id))

    def test_save_old_country_to_new_country(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving an existing venue with a
        # different country
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            venue = Venue(name="ABC", city="ABC", country="ITA", altitude="50", picture="lorem ipsum.png")
            venue.save()
            venue.country = "FRA"
            venue.save()
            self.assertEqual(venue.picture, "venues/%s/%s.png" % (venue.country, venue.venue_id))

    def test_save_old_to_blank_picture(self):
        #
        # save() returns the correctly formatted image filename and
        # location when saving an existing venue and removing
        # its picture
        #
        with patch('os.replace') as MockClass:
            instance = MockClass.return_value
            venue = Venue(name="ABC", city="ABC", country="ITA", altitude="50", picture="lorem ipsum.png")
            venue.save()
            venue.picture = ""
            venue.save()
            self.assertEqual(venue.picture, "")
