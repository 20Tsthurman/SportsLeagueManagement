from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import League, Team, Player, Match
from .forms import TeamForm, LeagueForm, PlayerForm, MatchForm
from django.db.models import Count, Sum
from django.views.generic import TemplateView
from .models import Division


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

# League Views
class LeagueListView(ListView):
    model = League
    template_name = 'league_management/league_list.html'
    context_object_name = 'leagues'

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

# Player Views
class PlayerListView(ListView):
    model = Player
    template_name = 'league_management/player_list.html'
    context_object_name = 'players'

class PlayerCreateView(CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'league_management/player_form.html'
    success_url = reverse_lazy('league_management:player-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.success_url)

class PlayerUpdateView(UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'league_management/player_form.html'
    success_url = reverse_lazy('league_management:player-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.success_url)

class PlayerDeleteView(DeleteView):
    model = Player
    template_name = 'league_management/player_confirm_delete.html'
    success_url = reverse_lazy('league_management:player-list')

# Match Views
class MatchListView(ListView):
    model = Match
    template_name = 'league_management/match_list.html'
    context_object_name = 'matches'

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
        
        # Get all divisions to organize standings by division
        divisions = Division.objects.all()
        standings_by_division = {}
        
        for division in divisions:
            teams = Team.objects.filter(division=division)
            division_standings = []
            
            for team in teams:
                # Get all matches for this team
                matches = Match.objects.filter(
                    teammatch__team=team,
                    status='Completed'  # Only count completed matches
                ).distinct()
                
                wins = 0
                losses = 0
                
                for match in matches:
                    team_score = TeamMatch.objects.get(match=match, team=team).score
                    opponent_score = TeamMatch.objects.get(
                        match=match, 
                        team__in=match.teams.exclude(id=team.id)
                    ).score
                    
                    if team_score is not None and opponent_score is not None:
                        if team_score > opponent_score:
                            wins += 1
                        elif team_score < opponent_score:
                            losses += 1
                
                division_standings.append({
                    'team': team,
                    'matches_played': wins + losses,
                    'wins': wins,
                    'losses': losses,
                    'points': wins * 3,  # 3 points for a win
                    'win_percentage': round(wins / (wins + losses) * 100, 2) if (wins + losses) > 0 else 0.0
                })
            
            # Sort division standings by points
            division_standings.sort(key=lambda x: (x['points'], x['win_percentage']), reverse=True)
            standings_by_division[division.name] = division_standings
        
        context['standings_by_division'] = standings_by_division
        return context