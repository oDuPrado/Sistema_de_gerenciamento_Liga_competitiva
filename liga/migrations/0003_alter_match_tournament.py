# Generated by Django 5.0.1 on 2024-01-14 05:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liga', '0002_tournament_tournamenttype_remove_match_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liga.tournament'),
        ),
    ]
