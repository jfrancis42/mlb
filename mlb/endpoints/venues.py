from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .._http import HTTPClient


@dataclass
class FieldInfo:
    capacity: Optional[int]
    turf_type: Optional[str]
    roof_type: Optional[str]
    left_line: Optional[int]
    left: Optional[int]
    left_center: Optional[int]
    center: Optional[int]
    right_center: Optional[int]
    right: Optional[int]
    right_line: Optional[int]
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "FieldInfo":
        return cls(
            capacity=d.get("capacity"),
            turf_type=d.get("turfType"),
            roof_type=d.get("roofType"),
            left_line=d.get("leftLine"),
            left=d.get("left"),
            left_center=d.get("leftCenter"),
            center=d.get("center"),
            right_center=d.get("rightCenter"),
            right=d.get("right"),
            right_line=d.get("rightLine"),
            raw=d,
        )


@dataclass
class Venue:
    id: int
    name: str
    city: Optional[str]
    state: Optional[str]
    state_abbrev: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    timezone_id: Optional[str]
    timezone_offset: Optional[int]
    field_info: Optional[FieldInfo]
    active: bool
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "Venue":
        loc = d.get("location", {})
        coords = loc.get("defaultCoordinates", {})
        tz = d.get("timeZone", {})
        fi = d.get("fieldInfo")
        return cls(
            id=d["id"],
            name=d["name"],
            city=loc.get("city"),
            state=loc.get("state"),
            state_abbrev=loc.get("stateAbbrev"),
            postal_code=loc.get("postalCode"),
            country=loc.get("country"),
            latitude=coords.get("latitude"),
            longitude=coords.get("longitude"),
            timezone_id=tz.get("id"),
            timezone_offset=tz.get("offset"),
            field_info=FieldInfo._from_dict(fi) if fi else None,
            active=d.get("active", True),
            raw=d,
        )


class VenuesEndpoint:
    def __init__(self, http: "HTTPClient"):
        self._http = http

    def list(
        self,
        venue_ids: Optional[list[int]] = None,
        sport_id: int = 1,
        season: Optional[int] = None,
        hydrate: Optional[list[str]] = None,
    ) -> list[Venue]:
        """List venues. Use venue_ids to fetch specific venues."""
        params: dict = {"sportId": sport_id}
        if venue_ids:
            params["venueIds"] = ",".join(str(i) for i in venue_ids)
        if season:
            params["season"] = season
        if hydrate:
            params["hydrate"] = ",".join(hydrate)
        data = self._http.get("venues", **params)
        return [Venue._from_dict(v) for v in data.get("venues", [])]

    def get(
        self,
        venue_id: int,
        season: Optional[int] = None,
        hydrate: Optional[list[str]] = None,
    ) -> Venue:
        """Return a single venue with full detail (location, fieldInfo, timezone)."""
        if hydrate is None:
            hydrate = ["location", "fieldInfo", "timezone"]
        results = self.list(venue_ids=[venue_id], season=season, hydrate=hydrate)
        if not results:
            from ..exceptions import MLBNotFoundError
            raise MLBNotFoundError(404, f"Venue {venue_id} not found")
        return results[0]
