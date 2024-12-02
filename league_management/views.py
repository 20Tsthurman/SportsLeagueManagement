from django.shortcuts import render
from django.views.generic import ListView
from .models import League, Team, Player, Match

def home(request):
    leagues = League.objects.all()
    return render(request, 'league_management/home.html', {'leagues': leagues})

class LeagueListView(ListView):
    model = League
    template_name = 'league_management/league_list.html'
    context_object_name = 'leagues'

class TeamListView(ListView):
    model = Team
    template_name = 'league_management/team_list.html'
    context_object_name = 'teams'

class PlayerListView(ListView):
    model = Player
    template_name = 'league_management/player_list.html'
    context_object_name = 'players'

class MatchListView(ListView):
    model = Match
    template_name = 'league_management/match_list.html'
    context_object_name = 'matches'