from django import forms
from .models import Division, Team, League, Player, Match, PlaysFor, TeamMatch 
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

class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ['name', 'level', 'league']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.TextInput(attrs={'class': 'form-control'}),
            'league': forms.Select(attrs={'class': 'form-control'}),
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
    home_team_score = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Home Team Score"
    )
    away_team_score = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Away Team Score"
    )
    
    class Meta:
        model = Match
        fields = ['date', 'time', 'status', 'season', 'home_team', 'away_team', 'home_team_score', 'away_team_score']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'season': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        home_team = cleaned_data.get('home_team')
        away_team = cleaned_data.get('away_team')
        status = cleaned_data.get('status')
        home_team_score = cleaned_data.get('home_team_score')
        away_team_score = cleaned_data.get('away_team_score')
        
        if home_team and away_team and home_team == away_team:
            raise forms.ValidationError("Home team and away team must be different.")
        
        if status == 'Completed':
            if home_team_score is None or away_team_score is None:
                raise forms.ValidationError("Scores must be provided for completed matches.")
            
        return cleaned_data

    def save(self, commit=True):
        match = super().save(commit=True)
        
        # Create or update TeamMatch instances
        home_team = self.cleaned_data['home_team']
        away_team = self.cleaned_data['away_team']
        home_team_score = self.cleaned_data.get('home_team_score')
        away_team_score = self.cleaned_data.get('away_team_score')
        
        # Update or create home team match
        TeamMatch.objects.update_or_create(
            match=match,
            team=home_team,
            defaults={
                'is_home_team': True,
                'score': home_team_score
            }
        )
        
        # Update or create away team match
        TeamMatch.objects.update_or_create(
            match=match,
            team=away_team,
            defaults={
                'is_home_team': False,
                'score': away_team_score
            }
        )
        
        return match