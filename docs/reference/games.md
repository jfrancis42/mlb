# Games

`client.games` — `GamesEndpoint`

The games endpoint works with `gamePk` — the unique game ID from the schedule.

```python
schedule = client.schedule.today()
game_pk = schedule.games[0].game_pk
```

## Methods

### `live_feed(game_pk, time_code=None) → LiveFeed`

Full live game data. Uses the `v1.1` API endpoint.

```python
feed = client.games.live_feed(777483)
```

`time_code`: replay state at a specific moment (format: `"YYYYMMDD_HHMMSS"`).

> **Note:** For an invalid/unknown `game_pk`, the API returns an empty-but-valid
> structure with `status_detail="Unknown"` rather than raising an error.

### `linescore(game_pk) → Linescore`

Just the linescore — faster than a full live feed when you only need the score.

### `boxscore(game_pk) → dict`

Full boxscore. Returns a raw dict — the structure is deeply nested with
per-player batting/pitching lines. Key paths:

```python
bs = client.games.boxscore(game_pk)
bs["teams"]["away"]["batters"]       # list of player IDs
bs["teams"]["away"]["players"]       # dict keyed by "ID123456"
bs["teams"]["away"]["teamStats"]     # team totals
bs["info"]                           # game info notes
bs["officials"]                      # umpires
```

### `play_by_play(game_pk) → dict`

All plays for the game. Returns the `liveData.plays` sub-object from the live feed.

```python
plays = client.games.play_by_play(game_pk)
all_plays = plays["allPlays"]        # list of all at-bats/events
current_play = plays["currentPlay"]  # live game only
```

### `content(game_pk) → dict`

Editorial content, highlights, and media assets. Raw dict.

### `diff_patch(game_pk, start_time, end_time) → dict`

Efficient polling: returns only fields that changed between two timestamps.
Useful for live-updating UIs — avoids re-fetching the entire feed.

```python
# Poll every 30 seconds
diff = client.games.diff_patch(
    game_pk,
    start_time="20260427_200000",
    end_time="20260427_200030",
)
```

## Return types

### `LiveFeed`
| Field | Type | Description |
|-------|------|-------------|
| `game_pk` | `int` | |
| `game_type` | `str` | `"R"`, `"P"`, etc. |
| `season` | `str` | Year |
| `game_date` | `str` | ISO datetime with timezone |
| `status_code` | `str` | |
| `status_detail` | `str` | e.g. `"In Progress"`, `"Final"` |
| `abstract_state` | `str` | `"Preview"`, `"Live"`, `"Final"` |
| `away_team_id` | `int` | |
| `away_team_name` | `str` | |
| `home_team_id` | `int` | |
| `home_team_name` | `str` | |
| `venue_id` | `int?` | |
| `venue_name` | `str?` | |
| `weather` | `Weather?` | |
| `game_info` | `GameInfo?` | Attendance, duration |
| `linescore` | `Linescore?` | |
| `probable_pitcher_away` | `dict?` | Player stub |
| `probable_pitcher_home` | `dict?` | Player stub |
| `decisions` | `dict?` | Win/loss/save pitchers |
| `flags` | `dict` | No-hitter, perfect game flags |
| `is_no_hitter` | `bool` | Property |
| `is_perfect_game` | `bool` | Property |
| `raw` | `dict` | Full API response |

### `Linescore`
| Field | Type |
|-------|------|
| `current_inning` | `int?` |
| `current_inning_ordinal` | `str?` | e.g. `"7th"` |
| `inning_state` | `str?` | `"Top"`, `"Middle"`, `"Bottom"`, `"End"` |
| `inning_half` | `str?` | `"Top"` or `"Bottom"` |
| `is_top_inning` | `bool?` | |
| `scheduled_innings` | `int` | |
| `innings` | `list[LinescoreInning]` | Per-inning breakdown |
| `away` | `LinescoreTotals` | R/H/E totals |
| `home` | `LinescoreTotals` | R/H/E totals |
| `balls` | `int` | |
| `strikes` | `int` | |
| `outs` | `int` | |

### `LinescoreInning`
| Field | Type |
|-------|------|
| `num` | `int` | Inning number |
| `ordinal` | `str` | e.g. `"1st"` |
| `away_runs` | `int?` | `None` if not yet played |
| `home_runs` | `int?` | |
| `away_hits` | `int?` | |
| `home_hits` | `int?` | |
| `away_errors` | `int?` | |
| `home_errors` | `int?` | |

### `LinescoreTotals`
| Field | Type |
|-------|------|
| `runs` | `int` |
| `hits` | `int` |
| `errors` | `int` |
| `left_on_base` | `int` |

### `Weather`
| Field | Type |
|-------|------|
| `condition` | `str?` | e.g. `"Clear"`, `"Cloudy"` |
| `temp` | `str?` | e.g. `"72"` (Fahrenheit) |
| `wind` | `str?` | e.g. `"5 mph, Out To CF"` |

### `GameInfo`
| Field | Type |
|-------|------|
| `attendance` | `int?` | |
| `first_pitch` | `str?` | ISO datetime |
| `duration_minutes` | `int?` | |
