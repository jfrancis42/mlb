from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .._http import HTTPClient


@dataclass
class Division:
    id: int
    name: str
    name_short: str
    abbreviation: str
    league_id: Optional[int]
    sport_id: Optional[int]
    active: bool
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "Division":
        return cls(
            id=d["id"],
            name=d["name"],
            name_short=d.get("nameShort", ""),
            abbreviation=d.get("abbreviation", ""),
            league_id=d.get("league", {}).get("id"),
            sport_id=d.get("sport", {}).get("id"),
            active=d.get("active", True),
            raw=d,
        )


class DivisionsEndpoint:
    # Well-known division IDs
    AL_EAST = 201
    AL_CENTRAL = 202
    AL_WEST = 200
    NL_EAST = 204
    NL_CENTRAL = 205
    NL_WEST = 203

    def __init__(self, http: "HTTPClient"):
        self._http = http

    def list(
        self,
        sport_id: int = 1,
        league_id: Optional[int] = None,
        division_id: Optional[int] = None,
    ) -> list[Division]:
        """List divisions, optionally filtered by league or specific division."""
        params: dict = {"sportId": sport_id}
        if league_id:
            params["leagueId"] = league_id
        if division_id:
            params["divisionId"] = division_id
        data = self._http.get("divisions", **params)
        return [Division._from_dict(d) for d in data.get("divisions", [])]

    def get(self, division_id: int) -> Division:
        """Return a single division by ID."""
        results = self.list(division_id=division_id)
        if not results:
            from ..exceptions import MLBNotFoundError
            raise MLBNotFoundError(404, f"Division {division_id} not found")
        return results[0]
