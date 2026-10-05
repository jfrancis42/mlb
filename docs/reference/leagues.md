# Leagues

`client.leagues` — `LeaguesEndpoint`

## Constants

```python
LeaguesEndpoint.AL = 103   # American League
LeaguesEndpoint.NL = 104   # National League
```

## Methods

### `list(sport_id=1, season=None, league_ids=None) → list[League]`

```python
leagues = client.leagues.list()                        # all MLB leagues
al_nl = client.leagues.list(league_ids=[103, 104])     # AL + NL only
```

### `get(league_id, season=None) → League`

```python
al = client.leagues.get(103)
nl = client.leagues.get(104)
```

## Return types

### `League`
| Field | Type |
|-------|------|
| `id` | `int` |
| `name` | `str` |
| `abbreviation` | `str` |
| `name_short` | `str` |
| `season` | `str?` |
| `num_teams` | `int` |
| `num_games` | `int` |
| `has_wild_card` | `bool` |
| `active` | `bool` |
| `season_dates` | `SeasonDates?` |
| `raw` | `dict` |

### `SeasonDates`
| Field | Type |
|-------|------|
| `season_id` | `str` |
| `pre_season_start` | `str?` |
| `pre_season_end` | `str?` |
| `season_start` | `str?` |
| `regular_season_start` | `str?` |
| `all_star_date` | `str?` |
| `regular_season_end` | `str?` |
| `post_season_start` | `str?` |
| `post_season_end` | `str?` |
| `season_end` | `str?` |
| `raw` | `dict` |
