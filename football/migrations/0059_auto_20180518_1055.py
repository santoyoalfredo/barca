# Generated by Django 2.0.2 on 2018-05-18 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0058_auto_20180518_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football.Season'),
        ),
        migrations.AlterField(
            model_name='season',
            name='competition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='football.Competition'),
        ),
    ]