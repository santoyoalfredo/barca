# Generated by Django 2.0.2 on 2018-02-07 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0007_auto_20180207_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='portrait',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
    ]
