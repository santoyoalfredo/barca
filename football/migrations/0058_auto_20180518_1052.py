# Generated by Django 2.0.2 on 2018-05-18 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0057_auto_20180517_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season', to='football.Season'),
        ),
    ]
