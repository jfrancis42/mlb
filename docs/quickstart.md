# Quickstart

## Installation

```bash
pip install mlb-stats-sdk
```

## Create a client

```python
from mlb import MLBClient

# Default: 30s timeout, 3 retries on 5xx, no rate limiting
client = MLBClient()

# Slower polling (be polite to the API)
client = MLBClient(rate_limit_delay=0.1)
```

## Today's schedule

```python
schedule = client.schedule.today()

print(f"{schedule.total_games} games today, {schedule.total_games_in_progress} in progress")

for game in schedule.games:
    score = ""
    if game.status.is_live or game.status.is_final:
        score = f" {game.away.score}-{game.home.score}"
    print(f"{game.away.team_name} @ {game.home.team_name}{score}  [{game.status.detailed_state}]")
```

## Schedule for a date range

```python
from datetime import date

schedule = client.schedule.get(
    start_date=date(2026, 4, 1),
    end_date=date(2026, 4, 30),
    team_id=client.teams.DODGERS,
)

for game in schedule.games:
    print(f"{game.official_date}  {game.away.team_name} @ {game.home.team_name}")
```

## Look up a team

```python
dodgers = client.teams.get(119)
print(dodgers.name)            # Los Angeles Dodgers
print(dodgers.abbreviation)    # LAD
print(dodgers.division_name)   # National League West
print(dodgers.venue_name)      # Dodger Stadium

# Or use the constant:
dodgers = client.teams.get(client.teams.DODGERS)
```

## Rosters

```python
# Active roster (26-man)
roster = client.teams.roster(119)
for player in roster:
    print(f"#{player.jersey_number}  {player.person_name}  {player.position_abbreviation}")

# 40-man roster
roster_40 = client.teams.roster(119, roster_type="40Man")

# Roster on a specific date
old_roster = client.teams.roster(119, date="2026-04-01")
```

## Look up a player

```python
ohtani = client.players.get(660271)
print(ohtani.full_name)         # Shohei Ohtani
print(ohtani.primary_position.name)  # Designated Hitter
print(ohtani.bat_side.description)   # Left
print(ohtani.pitch_hand.description) # Left

# Search by name
results = client.players.search("ohtani")
ohtani = results[0]
```

## Player stats

```python
# Current season hitting stats
stats = client.players.stats(
    660271,
    groups=["hitting"],
    stat_type="season",
    season=2026,
)
for group in stats:
    for split in group.splits:
        s = split.stat
        print(f"AVG {s.get('avg')}  HR {s.get('homeRuns')}  RBI {s.get('rbi')}")

# Career stats
career = client.players.career_stats(660271, groups=["hitting"])

# Season-by-season
yby = client.players.year_by_year(660271, groups=["hitting"])
for group in yby:
    for split in group.splits:
        print(f"{split.season}: {split.stat.get('avg')} AVG, {split.stat.get('homeRuns')} HR")
```

## Standings

```python
# Full MLB standings (all 6 divisions)
standings = client.standings.get()

for division in standings:
    print(f"\nDivision {division.division_id}:")
    for tr in division.team_records:
        gb = tr.games_back if tr.games_back != "-" else " -- "
        print(f"  {tr.division_rank}. {tr.team_name:25s} {tr.wins}-{tr.losses}  GB: {gb}")

# American League only
al = client.standings.get(league_ids=[103])

# Wild card
wc = client.standings.wild_card()
```

## Live game data

```python
# Get a gamePk from the schedule
schedule = client.schedule.today()
game = schedule.games[0]

# Full live feed (use v1.1 internally)
feed = client.games.live_feed(game.game_pk)
print(f"{feed.away_team_name} @ {feed.home_team_name}")
print(f"Status: {feed.status_detail}")
if feed.linescore:
    ls = feed.linescore
    print(f"Score: {ls.away.runs}-{ls.home.runs}")
    print(f"Inning: {ls.current_inning_ordinal} {ls.inning_half}")
    print(f"Count: {ls.balls}-{ls.strikes}, {ls.outs} outs")

# Just the linescore
linescore = client.games.linescore(game.game_pk)

# Boxscore (raw dict — structure is complex)
boxscore = client.games.boxscore(game.game_pk)
away_batters = boxscore["teams"]["away"]["batters"]

# Play-by-play
plays = client.games.play_by_play(game.game_pk)
last_play = plays["allPlays"][-1]

# Efficient polling: only changed fields since last check
diff = client.games.diff_patch(
    game.game_pk,
    start_time="20260427_200000",
    end_time="20260427_200500",
)
```

## Venues

```python
venue = client.venues.get(22)  # Dodger Stadium
print(venue.name)               # Dodger Stadium
print(venue.city)               # Los Angeles
print(f"{venue.latitude}, {venue.longitude}")

fi = venue.field_info
print(f"Capacity: {fi.capacity}")
print(f"CF: {fi.center} ft")
print(f"Turf: {fi.turf_type}, Roof: {fi.roof_type}")
```

## Well-known IDs

### Team IDs (via `client.teams.CONSTANT`)

| Constant | ID |
|----------|----|
| `DODGERS` | 119 |
| `YANKEES` | 147 |
| `RED_SOX` | 111 |
| `CUBS` | 112 |
| `ASTROS` | 117 |
| `BRAVES` | 144 |
| ... | ... |

### League IDs

| League | ID |
|--------|----|
| American League | 103 |
| National League | 104 |

### Division IDs (via `client.divisions.CONSTANT`)

| Constant | ID |
|----------|----|
| `AL_EAST` | 201 |
| `AL_CENTRAL` | 202 |
| `AL_WEST` | 200 |
| `NL_EAST` | 204 |
| `NL_CENTRAL` | 205 |
| `NL_WEST` | 203 |

## Accessing raw API data

Every model exposes `.raw` with the full original dict:

```python
team = client.teams.get(119)
raw_spring_league = team.raw["springLeague"]

feed = client.games.live_feed(game_pk)
all_players = feed.raw["gameData"]["players"]
```
