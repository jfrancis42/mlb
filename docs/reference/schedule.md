# Schedule

`client.schedule` — `ScheduleEndpoint`

## Methods

### `get(...) → Schedule`

```python
client.schedule.get(
    date=None,           # DateLike (str "YYYY-MM-DD", date, or datetime)
    start_date=None,     # DateLike — use with end_date for a range
    end_date=None,       # DateLike
    team_id=None,        # int — filter to one team
    sport_id=1,          # int — default MLB
    game_type=None,      # str — see Game Types below
    season=None,         # int — e.g. 2026
    hydrate=None,        # list[str] — see Hydrations below
) -> Schedule
```

If no date or range is given, returns today's schedule.

### `today(sport_id=1, hydrate=None) → Schedule`

Convenience wrapper for `get()` with no date.

### `for_team(team_id, season=None, game_type="R") → Schedule`

Full schedule for a specific team. Returns all dates in the season.

## Return types

### `Schedule`
| Field | Type | Description |
|-------|------|-------------|
| `total_items` | `int` | Total items returned |
| `total_games` | `int` | Number of games |
| `total_games_in_progress` | `int` | Live games |
| `dates` | `list[ScheduleDate]` | Per-date containers |
| `games` | `list[ScheduledGame]` | Flat list across all dates |

### `ScheduleDate`
| Field | Type |
|-------|------|
| `date` | `str` |
| `total_games` | `int` |
| `total_games_in_progress` | `int` |
| `games` | `list[ScheduledGame]` |

### `ScheduledGame`
| Field | Type | Description |
|-------|------|-------------|
| `game_pk` | `int` | Unique game ID |
| `game_guid` | `str` | UUID |
| `game_type` | `str` | See Game Types |
| `season` | `str` | Season year |
| `game_date` | `str` | ISO datetime with timezone |
| `official_date` | `str` | YYYY-MM-DD local date |
| `status` | `GameStatus` | Current game state |
| `away` | `ScheduleTeam` | Away team info |
| `home` | `ScheduleTeam` | Home team info |
| `venue_id` | `int?` | |
| `venue_name` | `str?` | |
| `day_night` | `str` | `"day"` or `"night"` |
| `scheduled_innings` | `int` | Usually 9 |
| `games_in_series` | `int` | |
| `series_game_number` | `int` | |
| `double_header` | `str` | `"N"`, `"Y"`, or `"S"` |
| `is_double_header` | `bool` | Property |

### `GameStatus`
| Field | Type |
|-------|------|
| `abstract_state` | `str` | `"Preview"`, `"Live"`, `"Final"` |
| `coded_state` | `str` | Single-char code |
| `detailed_state` | `str` | e.g. `"In Progress"`, `"Final"` |
| `status_code` | `str` | |
| `start_time_tbd` | `bool` | |
| `is_final` | `bool` | Property |
| `is_live` | `bool` | Property |
| `is_preview` | `bool` | Property |

### `ScheduleTeam`
| Field | Type |
|-------|------|
| `team_id` | `int` |
| `team_name` | `str` |
| `score` | `int?` | `None` before game starts |
| `wins` | `int` |
| `losses` | `int` |
| `win_pct` | `str` |
| `is_winner` | `bool?` | `None` until final |

## Game Types

| Code | Description |
|------|-------------|
| `R` | Regular Season |
| `S` | Spring Training |
| `P` | Postseason (all rounds) |
| `F` | Wild Card |
| `D` | Division Series |
| `L` | League Championship Series |
| `W` | World Series |
| `A` | All-Star Game |
| `E` | Exhibition |

## Hydrations

Pass `hydrate=["key1", "key2"]` to include additional data:

| Hydration | Description |
|-----------|-------------|
| `linescore` | In-progress/final score by inning |
| `team` | Expanded team info |
| `venue` | Venue details |
| `decisions` | Win/loss/save pitchers |
| `probablePitcher` | Probable starters |
| `broadcasts` | TV/radio broadcasts |
| `tickets` | Ticket links |
