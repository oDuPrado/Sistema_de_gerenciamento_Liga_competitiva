# Generated by Django 5.0.1 on 2024-01-26 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liga', '0009_tournament_results'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='player',
        ),
        migrations.RemoveField(
            model_name='deck',
            name='tournament',
        ),
    ]
