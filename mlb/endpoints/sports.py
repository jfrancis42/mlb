from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .._http import HTTPClient


@dataclass
class Sport:
    id: int
    name: str
    code: str
    abbreviation: str
    sort_order: int
    active: bool
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "Sport":
        return cls(
            id=d["id"],
            name=d["name"],
            code=d["code"],
            abbreviation=d["abbreviation"],
            sort_order=d.get("sortOrder", 0),
            active=d.get("activeStatus", True),
            raw=d,
        )


class SportsEndpoint:
    MLB = 1

    def __init__(self, http: "HTTPClient"):
        self._http = http

    def list(self, sport_id: Optional[int] = None) -> list[Sport]:
        """Return all sports, optionally filtered to a single sport."""
        params = {}
        if sport_id is not None:
            params["sportId"] = sport_id
        data = self._http.get("sports", **params)
        return [Sport._from_dict(s) for s in data.get("sports", [])]

    def get(self, sport_id: int) -> Sport:
        """Return a single sport by ID."""
        results = self.list(sport_id=sport_id)
        if not results:
            from ..exceptions import MLBNotFoundError
            raise MLBNotFoundError(404, f"Sport {sport_id} not found")
        return results[0]
