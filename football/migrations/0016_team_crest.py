# Generated by Django 2.0.2 on 2018-02-15 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0015_auto_20180207_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='crest',
            field=models.ImageField(blank=True, default='', null=True, upload_to='resources/teams'),
        ),
    ]
