# Players

`client.players` — `PlayersEndpoint`

## Methods

### `get(player_id, season=None) → Player`

Look up a player by their MLB player ID.

```python
ohtani = client.players.get(660271)
```

### `get_many(player_ids, season=None) → list[Player]`

Fetch multiple players in a single API call.

```python
players = client.players.get_many([660271, 592450, 665742])
```

### `search(name, sport_id=1, active=None) → list[Player]`

Search by name. Returns partial matches. Case-insensitive.

```python
results = client.players.search("ohtani")
results = client.players.search("judge", active=True)
```

### `stats(player_id, groups=None, stat_type="season", season=None, game_type="R") → list[StatGroup]`

Fetch player statistics.

**groups** (default: all three):
- `"hitting"`
- `"pitching"`
- `"fielding"`

**stat_type options:**

| Value | Description |
|-------|-------------|
| `"season"` | Current/specified season totals |
| `"career"` | Career cumulative |
| `"yearByYear"` | Season-by-season breakdown |
| `"gameLog"` | Game-by-game log |
| `"lastXGames"` | Last N games |
| `"byDateRange"` | Between two dates |
| `"vsPlayer"` | vs. a specific player |
| `"vsTeam"` | vs. a specific team |
| `"statsSingleSeason"` | Single-season with league context |

**game_type:** `"R"` (regular), `"P"` (postseason), `"S"` (spring), `"A"` (all-star)

### `career_stats(player_id, groups=None) → list[StatGroup]`

Shortcut for `stats(..., stat_type="career")`.

### `year_by_year(player_id, groups=None) → list[StatGroup]`

Shortcut for `stats(..., stat_type="yearByYear")`.

### `current_game_stats(player_id) → list[StatGroup]`

Stats from recent games.

## Return types

### `Player`
| Field | Type |
|-------|------|
| `id` | `int` |
| `full_name` | `str` |
| `first_name` | `str` |
| `last_name` | `str` |
| `use_name` | `str` | Preferred first name |
| `primary_number` | `str?` | Jersey number |
| `birth_date` | `str?` | YYYY-MM-DD |
| `current_age` | `int?` | |
| `birth_city` | `str?` | |
| `birth_country` | `str?` | |
| `height` | `str?` | e.g. "6' 4\"" |
| `weight` | `int?` | pounds |
| `active` | `bool` | |
| `primary_position` | `Position?` | |
| `mlb_debut_date` | `str?` | |
| `bat_side` | `Hand?` | |
| `pitch_hand` | `Hand?` | |
| `strike_zone_top` | `float?` | |
| `strike_zone_bottom` | `float?` | |
| `name_slug` | `str?` | URL-safe name |
| `raw` | `dict` | |

### `Position`
| Field | Type |
|-------|------|
| `code` | `str` | e.g. `"1"` (pitcher), `"2"` (catcher) |
| `name` | `str` | e.g. `"Pitcher"` |
| `type` | `str` | e.g. `"Pitcher"`, `"Infielder"` |
| `abbreviation` | `str` | e.g. `"P"` |

### `Hand`
| Field | Type |
|-------|------|
| `code` | `str` | `"L"`, `"R"`, `"S"` (switch) |
| `description` | `str` | e.g. `"Left"` |

### `StatGroup`
| Field | Type |
|-------|------|
| `group` | `str` | `"hitting"`, `"pitching"`, `"fielding"` |
| `type` | `str` | Display name of stat type |
| `splits` | `list[StatSplit]` | One per season/game/split |
| `raw` | `dict` | |

### `StatSplit`
| Field | Type |
|-------|------|
| `season` | `str?` | Year |
| `game_type` | `str?` | |
| `stat` | `dict` | The actual stats — varies by group |
| `team` | `dict?` | |
| `player` | `dict?` | |
| `position` | `dict?` | |
| `league` | `dict?` | |
| `raw` | `dict` | |

## Common stat fields

### Hitting (`split.stat`)
`gamesPlayed`, `atBats`, `runs`, `hits`, `doubles`, `triples`, `homeRuns`,
`rbi`, `stolenBases`, `caughtStealing`, `walks`, `strikeOuts`, `avg`,
`obp`, `slg`, `ops`, `babip`, `leftOnBase`

### Pitching (`split.stat`)
`wins`, `losses`, `era`, `gamesPlayed`, `gamesStarted`, `completeGames`,
`shutouts`, `saves`, `saveOpportunities`, `holds`, `blownSaves`,
`inningsPitched`, `hits`, `runs`, `earnedRuns`, `homeRuns`, `strikeOuts`,
`baseOnBalls`, `whip`, `strikeoutsPer9Inn`, `walksPer9Inn`

### Fielding (`split.stat`)
`gamesPlayed`, `gamesStarted`, `assists`, `putOuts`, `errors`,
`chances`, `fielding`, `doublePlays`, `rangeFactorPerGame`
