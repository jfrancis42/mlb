# mlb — Python SDK for the MLB Stats API

A small, typed Python client for [statsapi.mlb.com](https://statsapi.mlb.com),
the public (but undocumented) API behind MLB.com. No API key or account is
needed.

* Typed dataclasses for schedules, teams, rosters, players, standings,
  leagues, divisions, venues and games — with `.raw` on every model for
  anything not modelled.
* Retries on 5xx responses, optional rate limiting, and a small exception
  hierarchy (`MLBError`, `MLBNotFoundError`, `MLBRateLimitError`, ...).
* Depends only on `requests` and `urllib3`. Python 3.10+.

## Install

```bash
pip install mlb-stats-sdk
# or, from a checkout:
pip install -e .
```

The package is `mlb-stats-sdk`; the import name is `mlb`. (`mlb-statsapi` on
PyPI is a different, unrelated project.)

## Quick start

```python
from mlb import MLBClient

client = MLBClient()

# Today's games
for game in client.schedule.today().games:
    print(f"{game.away.team_name} @ {game.home.team_name}  [{game.status.detailed_state}]")

# A team's season, postseason included (the default is regular season only)
yankees = client.schedule.for_team(client.teams.YANKEES, season=2026, game_type="R,F,D,L,W")
for game in yankees.games[-5:]:
    print(game.official_date, game.away.team_name, game.away.score,
          "@", game.home.team_name, game.home.score)

# Standings (AL = 103, NL = 104)
for division in client.standings.get(league_ids=[103]):
    for tr in division.team_records:
        print(f"{tr.division_rank}. {tr.team_name} {tr.wins}-{tr.losses} {tr.games_back}")

# Extra data on any call: the API's `hydrate` parameter
sched = client.schedule.get(date="2026-10-05", hydrate=["venue(location)", "probablePitcher"])
```

See [`examples/yankees.py`](examples/yankees.py) for a fuller example
(roster, standings, recent results, season hitting stats).

## Choosing a season

**A season is a calendar year.** `season=2026` is everything played in 2026:
spring training (February-March), the regular season (late March-September)
and the postseason (October). Leave `season` out and you get the current one.

| Call | Selects the season with | Notes |
|------|-------------------------|-------|
| `schedule.for_team(team_id, season=2026)` | `season` | **Regular season only** by default; see game types below |
| `schedule.get(season=2026, team_id=...)` | `season` | Every game type unless `game_type` is given |
| `schedule.get(date="2026-10-05")` / `today()` | a date | That day's games |
| `schedule.get(start_date=..., end_date=...)` | a date range | Can cross seasons |
| `standings.get(season=2025)` | `season` | Final standings for a finished season; the current one so far if omitted |
| `teams.get(team_id, season=2025)` | `season` | The team as it was that year (name, league, venue) |
| `teams.roster(team_id, season=2025)` | `season` | Or `date="2026-04-01"` for the roster on one day |
| `teams.coaches(team_id, season=2025)`, `teams.stats(..., season=2025)` | `season` | |
| `players.stats(player_id, stat_type="season", season=2026)` | `season` | `career_stats()` and `year_by_year()` cover every season |

**Game types** (`game_type=`): `R` regular season, `F` wild card, `D`
division series, `L` league championship, `W` World Series, `S` spring
training, `E` exhibition, `A` All-Star Game. Give several as a comma list:

```python
client.schedule.for_team(147, season=2026)                         # regular season
client.schedule.for_team(147, season=2026, game_type="F,D,L,W")    # postseason only
client.schedule.for_team(147, season=2026, game_type="R,F,D,L,W")  # both
client.standings.get(season=2025, league_ids=[103])                # final 2025 AL standings
```

## Endpoints

| Attribute | Covers |
|-----------|--------|
| `client.schedule` | games by date, date range, team or season; `hydrate` |
| `client.teams` | teams, rosters, coaches, team stats |
| `client.players` | player info, search, season and career stats |
| `client.games` | live feed, linescore, boxscore, play-by-play |
| `client.standings` | division and wild-card standings |
| `client.leagues` | leagues and season dates |
| `client.divisions` | divisions |
| `client.venues` | ballparks, dimensions, location |
| `client.sports` | MLB, minor leagues and other sports |

Full reference: [`docs/`](docs/index.md).

## Things the API does that you might not expect

| Behaviour | Notes |
|-----------|-------|
| `for_team()` omits the postseason | Its `game_type` defaults to `"R"`; pass `"R,F,D,L,W"` |
| A rained-out game reports `abstractGameState: "Final"` | Check `codedGameState` / `detailedState` ("Cancelled", "Postponed") before treating a game as played |
| `standings?date=` returns HTTP 500 | Every date; `standings.as_of()` exists but the upstream call fails |
| `teams?divisionId=` is ignored | `teams.list(division_id=...)` filters client side |
| An unknown `gamePk` returns an empty live feed | Not a 404; `status_detail` is "Unknown" |
| The live feed is `v1.1`, everything else `v1` | Handled internally |
| A 40-man roster can list more than 40 | Injured-list placements |

## Tests

```bash
pip install -e '.[dev]'
python3 -m pytest tests -q
```

The tests are integration tests against the live API (no mocks), so they
need network access and their results can change with the season.

## Disclaimer

Not affiliated with or endorsed by Major League Baseball. MLB data is subject
to MLB Advanced Media's terms of use; this library only makes the requests.

## License

GNU General Public License v3.0 only (GPL-3.0-only) — see [LICENSE](LICENSE).
