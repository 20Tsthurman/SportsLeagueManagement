from django.db import models

class League(models.Model):
    name = models.CharField(max_length=100)
    sport_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Division(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='divisions')

    def __str__(self):
        return f"{self.league.name} - {self.name}"

class Season(models.Model):
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.year} Season"

    class Meta:
        ordering = ['-year']

class Team(models.Model):
    name = models.CharField(max_length=100)
    home_city = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    coach = models.CharField(max_length=100)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return self.name

class Player(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    dob = models.DateField()
    position = models.CharField(max_length=50)
    jersey_number = models.IntegerField()
    team = models.ManyToManyField(Team, through='PlaysFor')

    def __str__(self):
        return f"{self.fname} {self.lname}"

class Match(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Scheduled'
    )
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team, through='TeamMatch')

    def __str__(self):
        home_team = self.teammatch_set.filter(is_home_team=True).first()
        away_team = self.teammatch_set.filter(is_home_team=False).first()
        if home_team and away_team:
            return f"{home_team.team.name} vs {away_team.team.name} - {self.date}"
        return f"Match on {self.date}"

    def get_home_team(self):
        return self.teammatch_set.filter(is_home_team=True).first()

    def get_away_team(self):
        return self.teammatch_set.filter(is_home_team=False).first()

    def get_score_display(self):
        home_team = self.get_home_team()
        away_team = self.get_away_team()
        if home_team and away_team and home_team.score is not None and away_team.score is not None:
            return f"{home_team.team.name} {home_team.score} - {away_team.score} {away_team.team.name}"
        return "Score not available"

class TeamMatch(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    is_home_team = models.BooleanField()
    score = models.IntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ('team', 'match')


class PlaysFor(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('player', 'team')
