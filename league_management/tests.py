from league_management.models import League, Division, Team

# Create a league
league = League.objects.create(name="Test League", sport_type="Football")

# Create divisions
div1 = Division.objects.create(name="Division 1", level="First", league=league)
div2 = Division.objects.create(name="Division 2", level="Second", league=league)

# Create some teams
team1 = Team.objects.create(
    name="Team 1",
    home_city="City 1",
    founded_year=2000,
    coach="Coach 1",
    division=div1
)

# Verify data
print(League.objects.all())
print(Division.objects.all())
print(Team.objects.all())