# Generated by Django 2.0.2 on 2018-02-25 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0019_auto_20180224_2021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('position_id', models.AutoField(primary_key=True, serialize=False)),
                ('position', models.CharField(max_length=3)),
            ],
        ),
        migrations.AlterField(
            model_name='player',
            name='portrait',
            field=models.ImageField(blank=True, default='', null=True, upload_to='resources/players/'),
        ),
        migrations.RemoveField(
            model_name='player',
            name='position',
        ),
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.ManyToManyField(to='football.Position'),
        ),
    ]