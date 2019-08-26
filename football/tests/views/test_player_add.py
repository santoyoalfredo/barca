from django.test import TestCase
from django.urls import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile

from football.forms import PlayerAddForm
from football.models import Position

class PlayerAddTests(TestCase):

    #
	# The Player Add view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('playersadd'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The Players Add view should return the competition_add.html template
	# for rendering
	#
    def test_player_add(self):
        response = self.client.get(reverse_lazy('playersadd'))
        self.assertTemplateUsed(response=response, template_name='football/player_add.html', count=1)
    #
	# The Player Add view should display the correct form
	#
    def test_competition_add_form(self):
        form = PlayerAddForm()
        self.assertTrue('first_name' in form.fields)
        self.assertTrue('last_name' in form.fields)
        self.assertTrue('full_name' in form.fields)
        self.assertTrue('primary_positions' in form.fields)
        self.assertTrue('secondary_positions' in form.fields)
        self.assertTrue('club_number' in form.fields)
        self.assertTrue('country_number' in form.fields)
        self.assertTrue('dob' in form.fields)
        self.assertTrue('nationality' in form.fields)
        self.assertTrue('current_team' in form.fields)
        self.assertTrue('height' in form.fields)
        self.assertTrue('weight' in form.fields)
        self.assertTrue('portrait' in form.fields)
    #
	# The Player Add view should display help text for certain fields
	#
    def test_player_add_help(self):
        form = PlayerAddForm()
        self.assertEquals(form.fields['dob'].help_text, "YYYY-MM-DD")
        self.assertEquals(form.fields['nationality'].help_text, "FIFA Country Code")
        self.assertEquals(form.fields['height'].help_text, "cm")
        self.assertEquals(form.fields['weight'].help_text, "kg")
    #
	# The Player Add view should display an error when uploading an
    # unsupported image format for a logo
	#
    def test_player_add_error_logo(self):
        position = Position.objects.create(position='GK')
        small_gif = (
                b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
                b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
                b'\x02\x4c\x01\x00\x3b'
        )
        data = {'first_name': "Ipsum",
                'last_name': "Lorem",
                'full_name': "Ipsum Lorem",
                'primary_positions': position,
                'dob': "1999-01-01",
                'nationality': "USA",
                'height': 180,
                'weight': 180,
        }
        file_data = {
                        'portrait': SimpleUploadedFile('portrait.gif', small_gif, content_type='image/gif')
                    }
        form = PlayerAddForm(data, file_data)
        form.is_valid()
        self.assertTrue(form.has_error('portrait'), 'invalid')
