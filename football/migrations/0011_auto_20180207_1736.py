# Generated by Django 2.0.2 on 2018-02-07 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0010_competition_season'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('fixture_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('weather', models.CharField(choices=[('CLE', 'Clear'), ('CLO', 'Cloudy'), ('RAI', 'Rainy'), ('OVE', 'Overcast'), ('SUN', 'Sunny')], default='CLE', max_length=3)),
                ('temperature', models.DecimalField(decimal_places=1, max_digits=3)),
                ('windchill', models.DecimalField(decimal_places=1, max_digits=3)),
                ('humidity', models.IntegerField()),
                ('pressure', models.DecimalField(decimal_places=2, max_digits=4)),
                ('wind_direction', models.CharField(choices=[('N', 'North'), ('NNE', 'North-Northeast'), ('NE', 'Northeast'), ('ENE', 'East-Northeast'), ('E', 'East'), ('ESE', 'East-Southeast'), ('SE', 'Southeast'), ('SSE', 'South-Southeast'), ('S', 'South'), ('SSW', 'South-Southwest'), ('SW', 'Southwest'), ('WSW', 'West-Southwest'), ('W', 'West'), ('WNW', 'West-Northwest'), ('NW', 'Northwest'), ('NNW', 'North-Northwest'), ('V', 'Variable')], default='V', max_length=3)),
                ('wind_speed', models.DecimalField(decimal_places=1, max_digits=3)),
                ('home_score', models.IntegerField()),
                ('away_score', models.IntegerField()),
                ('extra_time', models.BooleanField()),
                ('penalty_shootout', models.BooleanField()),
                ('away_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='away_team', to='football.Team')),
                ('home_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='home_team', to='football.Team')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='football.Venue')),
                ('season_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='football.Season')),
            ],
        ),
        migrations.AlterField(
            model_name='competition',
            name='logo',
            field=models.ImageField(blank=True, default='', upload_to='resources/competitions/'),
        ),
    ]