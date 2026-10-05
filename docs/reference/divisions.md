# Divisions

`client.divisions` — `DivisionsEndpoint`

## Constants

```python
DivisionsEndpoint.AL_EAST    = 201
DivisionsEndpoint.AL_CENTRAL = 202
DivisionsEndpoint.AL_WEST    = 200
DivisionsEndpoint.NL_EAST    = 204
DivisionsEndpoint.NL_CENTRAL = 205
DivisionsEndpoint.NL_WEST    = 203
```

## Methods

### `list(sport_id=1, league_id=None, division_id=None) → list[Division]`

### `get(division_id) → Division`

## Return types

### `Division`
| Field | Type |
|-------|------|
| `id` | `int` |
| `name` | `str` |
| `name_short` | `str` |
| `abbreviation` | `str` |
| `league_id` | `int?` |
| `sport_id` | `int?` |
| `active` | `bool` |
| `raw` | `dict` |
