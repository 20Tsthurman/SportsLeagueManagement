# Generated by Django 5.1.3 on 2024-12-02 06:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sport_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('position', models.CharField(max_length=50)),
                ('jersey_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('level', models.CharField(max_length=50)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='divisions', to='league_management.league')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.CharField(max_length=50)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='league_management.season')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('home_city', models.CharField(max_length=100)),
                ('founded_year', models.IntegerField()),
                ('coach', models.CharField(max_length=100)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='league_management.division')),
            ],
        ),
        migrations.CreateModel(
            name='PlaysFor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league_management.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league_management.team')),
            ],
            options={
                'unique_together': {('player', 'team')},
            },
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ManyToManyField(through='league_management.PlaysFor', to='league_management.team'),
        ),
        migrations.CreateModel(
            name='TeamMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_home_team', models.BooleanField()),
                ('score', models.IntegerField(blank=True, null=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league_management.match')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league_management.team')),
            ],
            options={
                'unique_together': {('team', 'match')},
            },
        ),
        migrations.AddField(
            model_name='match',
            name='teams',
            field=models.ManyToManyField(through='league_management.TeamMatch', to='league_management.team'),
        ),
    ]