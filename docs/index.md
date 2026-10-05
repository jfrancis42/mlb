# MLB Stats API Python SDK

Python SDK for [statsapi.mlb.com](https://statsapi.mlb.com) — MLB's unofficial but
widely-used public Stats API. No API key or authentication required.

## Installation

```bash
pip install mlb-stats-sdk
```

## Quick example

```python
from mlb import MLBClient

client = MLBClient()

# Today's games
for game in client.schedule.today().games:
    print(f"{game.away.team_name} @ {game.home.team_name} — {game.status.detailed_state}")

# Division standings
for division in client.standings.get():
    print(f"\n{division.division_id}")
    for tr in division.team_records:
        print(f"  {tr.division_rank}. {tr.team_name} {tr.wins}-{tr.losses}")

# Player stats
ohtani = client.players.get(660271)
stats = client.players.year_by_year(660271, groups=["hitting"])
```

## Endpoints

| Attribute | What it covers |
|-----------|---------------|
| `client.schedule` | Game schedules, today/date/range/team |
| `client.teams` | Teams, rosters, coaches, stats |
| `client.players` | Player info, search, stats |
| `client.games` | Live feed, linescore, boxscore, play-by-play |
| `client.standings` | Division & wild card standings |
| `client.leagues` | League info, season dates |
| `client.divisions` | Division list |
| `client.venues` | Ballpark info, dimensions, coordinates |
| `client.sports` | Sport hierarchy (MLB, MiLB, etc.) |

## Reference docs

- [Schedule](reference/schedule.md)
- [Teams](reference/teams.md)
- [Players](reference/players.md)
- [Games](reference/games.md)
- [Standings](reference/standings.md)
- [Leagues](reference/leagues.md)
- [Divisions](reference/divisions.md)
- [Venues](reference/venues.md)
- [Sports](reference/sports.md)
- [Errors](reference/errors.md)
