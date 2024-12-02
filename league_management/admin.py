from django.contrib import admin
from .models import League, Division, Season, Team, Player, Match, PlaysFor, TeamMatch

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport_type')

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'league')

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('year', 'start_date', 'end_date')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'home_city', 'coach', 'division')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'position', 'jersey_number')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'status', 'season')

@admin.register(PlaysFor)
class PlaysForAdmin(admin.ModelAdmin):
    list_display = ('player', 'team', 'start_date', 'end_date')

@admin.register(TeamMatch)
class TeamMatchAdmin(admin.ModelAdmin):
    list_display = ('team', 'match', 'is_home_team', 'score')