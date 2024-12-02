from django import forms
from .models import Team, League, Player, Match, PlaysFor, TeamMatch 
from django.utils import timezone

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'home_city', 'founded_year', 'coach', 'division']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'home_city': forms.TextInput(attrs={'class': 'form-control'}),
            'founded_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'coach': forms.TextInput(attrs={'class': 'form-control'}),
            'division': forms.Select(attrs={'class': 'form-control'}),
        }

class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['name', 'sport_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sport_type': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PlayerForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=timezone.now().date()
    )

    class Meta:
        model = Player
        fields = ['fname', 'lname', 'dob', 'position', 'jersey_number', 'team', 'start_date']
        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control'}),
            'lname': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'jersey_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'team': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        # First save the player instance without the many-to-many relationship
        player = super().save(commit=False)
        if commit:
            player.save()
            # Handle the team relationships manually
            selected_teams = self.cleaned_data.get('team', [])
            start_date = self.cleaned_data.get('start_date')
            
            # Clear existing relationships
            PlaysFor.objects.filter(player=player).delete()
            
            # Create new relationships with start_date
            for team in selected_teams:
                PlaysFor.objects.create(
                    player=player,
                    team=team,
                    start_date=start_date
                )
        return player

class MatchForm(forms.ModelForm):
    home_team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Home Team"
    )
    away_team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Away Team"
    )
    
    class Meta:
        model = Match
        fields = ['status', 'home_team', 'away_team']  # Update this list
        widgets = {
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        home_team = cleaned_data.get('home_team')
        away_team = cleaned_data.get('away_team')
        
        if home_team and away_team and home_team == away_team:
            raise forms.ValidationError("Home team and away team must be different.")
            
        return cleaned_data
