# Generated by Django 2.0.2 on 2018-05-17 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0055_auto_20180517_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='location',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='football.Venue'),
        ),
    ]