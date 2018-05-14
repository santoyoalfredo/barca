from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *

class CompetitionAddForm(ModelForm):
    class Meta:
        model = Competition
        fields = ['competition_id', 'name', 'logo', 'competition_format', 'promotion_limit', 'qualifying_limit', 'relegation_limit']

    def clean_logo(self):
        logo = self.cleaned_data['logo']
        if logo:
            if not(logo.content_type == 'image/jpeg' or logo.content_type == 'image/png'):
                raise ValidationError(
                    ('Invalid file type. Please use a .jpg or .png file.'),
                    code='invalid'
                )

        return logo

    def clean(self):
        pass

    def add_competition(self):
        self.save()

class PlayerAddForm(ModelForm):
    class Meta:
        model = Player
        fields = ['player_id', 'first_name', 'last_name', 'full_name', 'primary_positions', 'secondary_positions', 'club_number', 'country_number', 'dob', 'nationality', 'current_team', 'height', 'weight', 'portrait']

    def clean_logo(self):
        logo = self.cleaned_data['portrait']
        if logo:
            if not(logo.content_type == 'image/jpeg' or logo.content_type == 'image/png'):
                raise ValidationError(
                    ('Invalid file type. Please use a .jpg or .png file.'),
                    code='invalid'
                )

        return logo

    def clean(self):
        pass

    def add_player(self):
        self.save()

class SeasonAddForm(ModelForm):
    class Meta:
        model = Season
        fields = ['season_id', 'competition', 'year', 'teams']

    def clean(self):
        pass

    def add_season(self):
        self.save()
