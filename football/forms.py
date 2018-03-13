from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *

class CompetitionAddForm(ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'logo', 'competition_format', 'promotion_limit', 'qualifying_limit', 'relegation_limit']

    def clean_logo(self):
        logo = self.cleaned_data['logo']
        if not (logo.name == 'None'):
            if not(logo.content_type == 'image/jpeg' or logo.content_type == 'image/png'):
                raise ValidationError(
                    ('Invalid file type. Please use a .jpg or .png file.'),
                    code='invalid'
                )

        return logo

    def clean(self):
        print(self.cleaned_data)

    def add_competition(self):
        #save model instance to database
        pass
