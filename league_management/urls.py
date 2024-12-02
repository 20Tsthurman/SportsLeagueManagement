from django.urls import path
from . import views

app_name = 'league_management'

urlpatterns = [
    path('', views.home, name='home'),
    path('leagues/', views.LeagueListView.as_view(), name='league-list'),
    path('teams/', views.TeamListView.as_view(), name='team-list'),
    path('players/', views.PlayerListView.as_view(), name='player-list'),
    path('matches/', views.MatchListView.as_view(), name='match-list'),
]