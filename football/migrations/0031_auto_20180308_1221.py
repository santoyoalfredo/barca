# Generated by Django 2.0.2 on 2018-03-08 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0030_auto_20180308_1212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competition',
            old_name='promotion_spots',
            new_name='promotion_limit',
        ),
        migrations.RenameField(
            model_name='competition',
            old_name='qualifying_spots',
            new_name='qualifying_limit',
        ),
        migrations.RenameField(
            model_name='competition',
            old_name='relegation_spots',
            new_name='relegation_limit',
        ),
        migrations.AlterField(
            model_name='competition',
            name='competition_format',
            field=models.CharField(choices=[('l', 'League'), ('k', 'Knockout')], default='l', max_length=1),
        ),
    ]