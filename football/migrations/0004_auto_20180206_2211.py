# Generated by Django 2.0.2 on 2018-02-07 03:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0003_auto_20180206_2208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='current_Team',
            new_name='current_team',
        ),
    ]