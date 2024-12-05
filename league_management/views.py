from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Count, Sum, Q
from .models import (
    League, 
    Team, 
    Player, 
    Match, 
    Division,
    Season,
    TeamMatch
)
from .forms import DivisionForm, TeamForm, LeagueForm, PlayerForm, MatchForm

def search_results(request):
    query = request.GET.get('q', '')
    teams = []
    players = []

    if query:
        # Search in teams
        teams = Team.objects.filter(
            Q(name__icontains=query) |
            Q(home_city__icontains=query) |
            Q(coach__icontains=query)
        )

        # Search in players
        players = Player.objects.filter(
            Q(fname__icontains=query) |
            Q(lname__icontains=query) |
            Q(position__icontains=query)
        )

    return render(request, 'league_management/search_results.html', {
        'query': query,
        'teams': teams,
        'players': players,
    })

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

class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'league_management/team_form.html'
    success_url = reverse_lazy('league_management:team-list')

class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'league_management/team_form.html'
    success_url = reverse_lazy('league_management:team-list')

class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'league_management/team_confirm_delete.html'
    success_url = reverse_lazy('league_management:team-list')

class LeagueCreateView(CreateView):
    model = League
    form_class = LeagueForm
    template_name = 'league_management/league_form.html'
    success_url = reverse_lazy('league_management:league-list')

class LeagueUpdateView(UpdateView):
    model = League
    form_class = LeagueForm
    template_name = 'league_management/league_form.html'
    success_url = reverse_lazy('league_management:league-list')

class LeagueDeleteView(DeleteView):
    model = League
    template_name = 'league_management/league_confirm_delete.html'
    success_url = reverse_lazy('league_management:league-list')

class PlayerCreateView(CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'league_management/player_form.html'
    success_url = reverse_lazy('league_management:player-list')

class PlayerUpdateView(UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'league_management/player_form.html'
    success_url = reverse_lazy('league_management:player-list')

class PlayerDeleteView(DeleteView):
    model = Player
    template_name = 'league_management/player_confirm_delete.html'
    success_url = reverse_lazy('league_management:player-list')

class MatchCreateView(CreateView):
    model = Match
    form_class = MatchForm
    template_name = 'league_management/match_form.html'
    success_url = reverse_lazy('league_management:match-list')

class MatchUpdateView(UpdateView):
    model = Match
    form_class = MatchForm
    template_name = 'league_management/match_form.html'
    success_url = reverse_lazy('league_management:match-list')

class MatchDeleteView(DeleteView):
    model = Match
    template_name = 'league_management/match_confirm_delete.html'
    success_url = reverse_lazy('league_management:match-list')

class LeagueStandingsView(TemplateView):
    template_name = 'league_management/standings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current season (or latest season)
        current_season = Season.objects.order_by('-year').first()
        
        if not current_season:
            context['no_season'] = True
            return context
            
        # Get all leagues
        leagues = League.objects.all()
        standings_by_league = {}
        
        for league in leagues:
            # Get divisions for this league
            divisions = Division.objects.filter(league=league)
            league_standings = {}
            
            for division in divisions:
                teams = Team.objects.filter(division=division)
                division_standings = []
                
                for team in teams:
                    team_matches = TeamMatch.objects.filter(
                        team=team,
                        match__season=current_season,
                        match__status='Completed'
                    ).select_related('match')

                    stats = {
                        'team': team,
                        'matches_played': 0,
                        'wins': 0,
                        'draws': 0,
                        'losses': 0,
                        'goals_for': 0,
                        'goals_against': 0,
                        'goal_difference': 0,
                        'points': 0
                    }

                    for tm in team_matches:
                        match = tm.match
                        opponent_tm = match.teammatch_set.exclude(team=team).first()
                        
                        if tm.score is not None and opponent_tm and opponent_tm.score is not None:
                            stats['matches_played'] += 1
                            stats['goals_for'] += tm.score
                            stats['goals_against'] += opponent_tm.score
                            
                            if tm.score > opponent_tm.score:
                                stats['wins'] += 1
                                stats['points'] += 3
                            elif tm.score == opponent_tm.score:
                                stats['draws'] += 1
                                stats['points'] += 1
                            else:
                                stats['losses'] += 1

                    # Calculate additional stats
                    stats['goal_difference'] = stats['goals_for'] - stats['goals_against']
                    if stats['matches_played'] > 0:
                        stats['win_percentage'] = round((stats['wins'] / stats['matches_played']) * 100, 2)
                    else:
                        stats['win_percentage'] = 0.0

                    division_standings.append(stats)

                # Sort division standings
                division_standings.sort(
                    key=lambda x: (
                        -x['points'],  # Primary sort: Points (descending)
                        -x['goal_difference'],  # Secondary sort: Goal difference (descending)
                        -x['goals_for'],  # Tertiary sort: Goals scored (descending)
                        x['team'].name.lower()  # Final sort: Alphabetically by team name
                    )
                )

                if division_standings:  # Only add divisions that have teams
                    league_standings[division.name] = division_standings
            
            if league_standings:  # Only add leagues that have divisions with teams
                standings_by_league[league.name] = {
                    'standings': league_standings,
                    'sport_type': league.sport_type
                }

        context['standings_by_league'] = standings_by_league
        context['current_season'] = current_season
        return context
    
class DivisionListView(ListView):
    model = Division
    template_name = 'league_management/division_list.html'
    context_object_name = 'divisions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group divisions by league
        divisions_by_league = {}
        for division in context['divisions']:
            if division.league not in divisions_by_league:
                divisions_by_league[division.league] = []
            divisions_by_league[division.league].append(division)
        context['divisions_by_league'] = divisions_by_league
        return context

class DivisionCreateView(CreateView):
    model = Division
    form_class = DivisionForm
    template_name = 'league_management/division_form.html'
    success_url = reverse_lazy('league_management:division-list')

class DivisionUpdateView(UpdateView):
    model = Division
    form_class = DivisionForm
    template_name = 'league_management/division_form.html'
    success_url = reverse_lazy('league_management:division-list')

class DivisionDeleteView(DeleteView):
    model = Division
    template_name = 'league_management/division_confirm_delete.html'
    success_url = reverse_lazy('league_management:division-list')