# Error Handling

All SDK exceptions inherit from `mlb.MLBError`.

## Exception hierarchy

```
MLBError
└── MLBHTTPError
    ├── MLBNotFoundError    (HTTP 404)
    ├── MLBRateLimitError   (HTTP 429)
    └── MLBServerError      (HTTP 5xx)
```

## Usage

```python
from mlb import MLBClient, MLBNotFoundError, MLBServerError, MLBError

client = MLBClient()

try:
    team = client.teams.get(99999)
except MLBNotFoundError as e:
    print(f"Not found: {e.status_code}")
except MLBServerError as e:
    print(f"MLB API is having issues: {e.status_code}")
except MLBError as e:
    print(f"Unexpected error: {e}")
```

## `MLBHTTPError` attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `status_code` | `int` | HTTP status code |
| `args[0]` | `str` | Human-readable message |

## Known quirks that do NOT raise exceptions

| Situation | Behavior |
|-----------|----------|
| Unknown `game_pk` | Returns empty `LiveFeed` with `status_detail="Unknown"` |
| `standings?date=` | Returns HTTP 500 → raises `MLBServerError` after retries |

## Retry behavior

The SDK automatically retries on HTTP 500, 502, 503, 504 with exponential
backoff. Default: 3 retries. Override at construction:

```python
client = MLBClient(max_retries=5)
client = MLBClient(max_retries=0)  # no retries
```
