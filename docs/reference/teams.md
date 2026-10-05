# Teams

`client.teams` — `TeamsEndpoint`

## Methods

### `list(...) → list[Team]`

```python
client.teams.list(
    sport_id=1,       # int — default MLB
    season=None,      # int
    league_id=None,   # int — 103 (AL) or 104 (NL)
    division_id=None, # int — filtered client-side (API ignores this param)
    active_status=None, # str — "Y", "N", or "B" (both)
) -> list[Team]
```

Returns all 30 active MLB teams by default.

### `get(team_id, season=None) → Team`

Single team by ID.

### `roster(team_id, roster_type="active", season=None, date=None) → list[RosterEntry]`

Fetch a team's roster.

**roster_type options:**

| Value | Description |
|-------|-------------|
| `"active"` | 26-man active roster |
| `"40Man"` | 40-man roster (may exceed 40 due to IL) |
| `"fullRoster"` | All players in org |
| `"depthChart"` | Depth chart order |
| `"gameday"` | Day-of-game roster |
| `"nonRosterInvitees"` | Spring training invitees |

### `coaches(team_id, season=None) → list[dict]`

Returns raw list of coaching staff.

### `stats(team_id, stat_type="season", groups=None, season=None) → dict`

Team statistics. Returns raw dict — structure varies by group.

## Team constants

```python
client.teams.DODGERS    # 119
client.teams.YANKEES    # 147
client.teams.RED_SOX    # 111
# ... all 30 teams
```

Full list: `ANGELS, ASTROS, ATHLETICS, BLUE_JAYS, BRAVES, BREWERS, CARDINALS,
CUBS, DIAMONDBACKS, DODGERS, GIANTS, GUARDIANS, MARINERS, MARLINS, METS,
NATIONALS, ORIOLES, PADRES, PHILLIES, PIRATES, RANGERS, RAYS, RED_SOX,
REDS, ROCKIES, ROYALS, TIGERS, TWINS, WHITE_SOX, YANKEES`

## Return types

### `Team`
| Field | Type |
|-------|------|
| `id` | `int` |
| `name` | `str` | Full name (e.g. "Los Angeles Dodgers") |
| `abbreviation` | `str` | e.g. "LAD" |
| `team_name` | `str` | e.g. "Dodgers" |
| `location_name` | `str` | e.g. "Los Angeles" |
| `short_name` | `str` | e.g. "LA Dodgers" |
| `franchise_name` | `str` | |
| `club_name` | `str` | |
| `team_code` | `str` | 3-char code |
| `file_code` | `str` | |
| `season` | `int?` | |
| `first_year_of_play` | `str?` | |
| `venue_id` | `int?` | |
| `venue_name` | `str?` | |
| `league_id` | `int?` | 103 or 104 |
| `league_name` | `str?` | |
| `division_id` | `int?` | |
| `division_name` | `str?` | |
| `sport_id` | `int?` | |
| `active` | `bool` | |
| `raw` | `dict` | Full API response |

### `RosterEntry`
| Field | Type |
|-------|------|
| `person_id` | `int` |
| `person_name` | `str` |
| `jersey_number` | `str?` |
| `position_code` | `str` |
| `position_name` | `str` |
| `position_type` | `str` |
| `position_abbreviation` | `str` |
| `status` | `str` | e.g. "Active", "Injured 15-Day" |
| `raw` | `dict` |
