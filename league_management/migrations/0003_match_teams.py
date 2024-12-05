# Generated by Django 5.1.3 on 2024-12-03 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_management', '0002_remove_match_teams_alter_match_season_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='teams',
            field=models.ManyToManyField(through='league_management.TeamMatch', to='league_management.team'),
        ),
    ]
