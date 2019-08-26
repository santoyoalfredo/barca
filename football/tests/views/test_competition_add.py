from django.test import TestCase
from django.urls import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile

from football.forms import CompetitionAddForm

class CompetitionAddTests(TestCase):

    #
	# The Competition Add view should return the base.html template
	# for rendering
	#
    def test_base(self):
        response = self.client.get(reverse_lazy('competitionsadd'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='football/base.html', count=1)
    #
	# The Competition Add view should return the competition_add.html template
	# for rendering
	#
    def test_competition_add(self):
        response = self.client.get(reverse_lazy('competitionsadd'))
        self.assertTemplateUsed(response=response, template_name='football/competition_add.html', count=1)
    #
	# The Competition Add view should display the correct form
	#
    def test_competition_add_form(self):
        form = CompetitionAddForm()
        self.assertTrue('name' in form.fields)
        self.assertTrue('logo' in form.fields)
        self.assertTrue('competition_format' in form.fields)
        self.assertTrue('promotion_limit' in form.fields)
        self.assertTrue('qualifying_limit' in form.fields)
        self.assertTrue('relegation_limit' in form.fields)
    #
	# The Competition Add view should display help text for certain fields
	#
    def test_competition_add_help(self):
        form = CompetitionAddForm()
        self.assertEquals(form.fields['competition_format'].help_text, "League (Double round-robin), Knockout (Single elimination, two fixtures per round except final")
        self.assertEquals(form.fields['promotion_limit'].help_text, "Final position for league promotion or competition entry")
        self.assertEquals(form.fields['qualifying_limit'].help_text, "Final position for competition entry or qualification")
        self.assertEquals(form.fields['relegation_limit'].help_text, "Number of relegation spots")
    #
	# The Competition Add view should display an error when uploading an
    # unsupported image format for a logo
	#
    def test_competition_add_error_logo(self):
        small_gif = (
                b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
                b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
                b'\x02\x4c\x01\x00\x3b'
        )
        data = {'name':'Ipsum',
                'competition_format':'l',
                'promotion_limit':3,
                'qualifying_limit':2,
                'relegation_limit':3
        }
        file_data = {
                        'logo': SimpleUploadedFile('logo.gif', small_gif, content_type='image/gif')
                    }
        form = CompetitionAddForm(data, file_data)
        form.is_valid()
        self.assertTrue(form.has_error('logo'), 'invalid')
