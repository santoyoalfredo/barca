# Generated by Django 2.0.2 on 2018-02-25 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0020_auto_20180225_1034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='position',
            new_name='positions',
        ),
    ]