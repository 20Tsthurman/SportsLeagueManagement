from django.urls import path
from . import views

app_name = 'league_management'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search'),
    
    # League URLs
    path('leagues/', views.LeagueListView.as_view(), name='league-list'),
    path('leagues/add/', views.LeagueCreateView.as_view(), name='league-create'),
    path('leagues/<int:pk>/edit/', views.LeagueUpdateView.as_view(), name='league-update'),
    path('leagues/<int:pk>/delete/', views.LeagueDeleteView.as_view(), name='league-delete'),
    
    # Team URLs
    path('teams/', views.TeamListView.as_view(), name='team-list'),
    path('teams/add/', views.TeamCreateView.as_view(), name='team-create'),
    path('teams/<int:pk>/edit/', views.TeamUpdateView.as_view(), name='team-update'),
    path('teams/<int:pk>/delete/', views.TeamDeleteView.as_view(), name='team-delete'),
    
    # Player URLs
    path('players/', views.PlayerListView.as_view(), name='player-list'),
    path('players/add/', views.PlayerCreateView.as_view(), name='player-create'),
    path('players/<int:pk>/edit/', views.PlayerUpdateView.as_view(), name='player-update'),
    path('players/<int:pk>/delete/', views.PlayerDeleteView.as_view(), name='player-delete'),
    
    # Match URLs
    path('matches/', views.MatchListView.as_view(), name='match-list'),
    path('matches/add/', views.MatchCreateView.as_view(), name='match-create'),
    path('matches/<int:pk>/edit/', views.MatchUpdateView.as_view(), name='match-update'),
    path('matches/<int:pk>/delete/', views.MatchDeleteView.as_view(), name='match-delete'),
    path('standings/', views.LeagueStandingsView.as_view(), name='standings'),

    #Divisions
    path('divisions/', views.DivisionListView.as_view(), name='division-list'),
    path('divisions/add/', views.DivisionCreateView.as_view(), name='division-create'),
    path('divisions/<int:pk>/edit/', views.DivisionUpdateView.as_view(), name='division-update'),
    path('divisions/<int:pk>/delete/', views.DivisionDeleteView.as_view(), name='division-delete'),
]