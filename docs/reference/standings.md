# Standings

`client.standings` — `StandingsEndpoint`

## Methods

### `get(...) → list[DivisionStandings]`

```python
client.standings.get(
    league_ids=[103, 104],      # list[int] — default both leagues
    season=None,                # int — default current season
    standings_type="regularSeason",  # str — see Standings Types
    date=None,                  # str YYYY-MM-DD — WARNING: see note below
    hydrate=None,               # list[str]
) -> list[DivisionStandings]
```

Returns one `DivisionStandings` per division — 6 total for all of MLB,
3 for a single league.

> **Warning:** The `date` parameter consistently returns HTTP 500 from the
> MLB API. Use `season` to get historical standings instead.

### `wild_card(season=None) → list[DivisionStandings]`

Wild card standings.

### `as_of(date, season=None) → list[DivisionStandings]`

Standings as of a specific date. Currently broken upstream (see warning above).

## Standings Types

| Value | Description |
|-------|-------------|
| `"regularSeason"` | Default — current regular season |
| `"wildCard"` | Wild card race |
| `"divisionLeaders"` | Division leaders only |
| `"firstHalf"` | First half (split-season leagues) |
| `"secondHalf"` | Second half |
| `"springTraining"` | Spring training |
| `"postseason"` | Postseason |

## Return types

### `DivisionStandings`
| Field | Type |
|-------|------|
| `standings_type` | `str` |
| `league_id` | `int?` |
| `division_id` | `int?` |
| `last_updated` | `str?` | ISO datetime |
| `team_records` | `list[TeamRecord]` | Ordered 1st→last in division |
| `raw` | `dict` | |

### `TeamRecord`
| Field | Type |
|-------|------|
| `team_id` | `int` |
| `team_name` | `str` |
| `season` | `str` |
| `division_rank` | `str` | `"1"` through `"5"` |
| `league_rank` | `str` |
| `sport_rank` | `str` |
| `games_played` | `int` |
| `games_back` | `str` | `"-"` for leader, `"1.5"` etc. |
| `wild_card_games_back` | `str` |
| `wins` | `int` |
| `losses` | `int` |
| `run_differential` | `int` |
| `winning_pct` | `str` | e.g. `".600"` |
| `streak` | `Streak?` |
| `league_record` | `LeagueRecord` |
| `division_champ` | `bool` |
| `division_leader` | `bool` |
| `wild_card_leader` | `bool` |
| `has_wildcard` | `bool` |
| `clinched` | `bool` |
| `elimination_number` | `str?` |
| `wild_card_elimination_number` | `str?` |
| `runs_scored` | `int` |
| `runs_allowed` | `int` |
| `raw` | `dict` |

### `Streak`
| Field | Type |
|-------|------|
| `code` | `str` | e.g. `"W3"` |
| `type` | `str` | `"wins"` or `"losses"` |
| `number` | `int` | |

### `LeagueRecord`
| Field | Type |
|-------|------|
| `wins` | `int` |
| `losses` | `int` |
| `ties` | `int` |
| `pct` | `str` |
