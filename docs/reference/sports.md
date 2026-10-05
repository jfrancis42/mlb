# Sports

`client.sports` — `SportsEndpoint`

The sports endpoint covers the hierarchy of baseball leagues in the Stats API:
MLB (id=1), AAA, AA, A+, A, Rookie, international leagues, etc.

## Constants

```python
SportsEndpoint.MLB = 1
```

## Methods

### `list(sport_id=None) → list[Sport]`

```python
all_sports = client.sports.list()      # all ~24 sports
mlb_only = client.sports.list(sport_id=1)
```

### `get(sport_id) → Sport`

## Common sport IDs

| ID | Name |
|----|------|
| 1 | Major League Baseball |
| 11 | Triple-A |
| 12 | Double-A |
| 13 | Class A Advanced |
| 14 | Class A |
| 16 | Rookie |

## Return types

### `Sport`
| Field | Type |
|-------|------|
| `id` | `int` |
| `name` | `str` |
| `code` | `str` |
| `abbreviation` | `str` |
| `sort_order` | `int` |
| `active` | `bool` |
| `raw` | `dict` |
