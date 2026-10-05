# Venues

`client.venues` — `VenuesEndpoint`

## Methods

### `list(...) → list[Venue]`

```python
client.venues.list(
    venue_ids=None,    # list[int] — specific venues
    sport_id=1,
    season=None,
    hydrate=None,      # list[str] — default none; get() auto-adds ["location","fieldInfo","timezone"]
) -> list[Venue]
```

### `get(venue_id, season=None, hydrate=None) → Venue`

Returns a single venue with location, field info, and timezone hydrated by default.

```python
dodger_stadium = client.venues.get(22)
yankee_stadium = client.venues.get(3313)
```

## Well-known venue IDs

| Venue | ID |
|-------|----|
| Dodger Stadium | 22 |
| Yankee Stadium | 3313 |
| Fenway Park | 3 |
| Wrigley Field | 17 |
| Oracle Park | 2395 |
| Camden Yards | 2 |
| T-Mobile Park | 680 |
| Coors Field | 19 |
| Globe Life Field | 5325 |
| Truist Park | 4705 |

## Return types

### `Venue`
| Field | Type |
|-------|------|
| `id` | `int` |
| `name` | `str` |
| `city` | `str?` |
| `state` | `str?` |
| `state_abbrev` | `str?` |
| `postal_code` | `str?` |
| `country` | `str?` |
| `latitude` | `float?` |
| `longitude` | `float?` |
| `timezone_id` | `str?` | e.g. `"America/Los_Angeles"` |
| `timezone_offset` | `int?` | Hours from UTC |
| `field_info` | `FieldInfo?` | Requires hydration |
| `active` | `bool` |
| `raw` | `dict` |

### `FieldInfo`
| Field | Type | Notes |
|-------|------|-------|
| `capacity` | `int?` | Seating capacity |
| `turf_type` | `str?` | `"Grass"`, `"ArtificialTurf"` |
| `roof_type` | `str?` | `"Open"`, `"Retractable"`, `"Dome"` |
| `left_line` | `int?` | Distance in feet |
| `left` | `int?` | |
| `left_center` | `int?` | |
| `center` | `int?` | |
| `right_center` | `int?` | |
| `right` | `int?` | |
| `right_line` | `int?` | |
| `raw` | `dict` | |
