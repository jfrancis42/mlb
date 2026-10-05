from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .._http import HTTPClient

# Well-known league IDs
AL = 103
NL = 104


@dataclass
class SeasonDates:
    season_id: str
    pre_season_start: Optional[str]
    pre_season_end: Optional[str]
    season_start: Optional[str]
    regular_season_start: Optional[str]
    all_star_date: Optional[str]
    regular_season_end: Optional[str]
    post_season_start: Optional[str]
    post_season_end: Optional[str]
    season_end: Optional[str]
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "SeasonDates":
        return cls(
            season_id=d.get("seasonId", ""),
            pre_season_start=d.get("preSeasonStartDate"),
            pre_season_end=d.get("preSeasonEndDate"),
            season_start=d.get("seasonStartDate"),
            regular_season_start=d.get("regularSeasonStartDate"),
            all_star_date=d.get("allStarDate"),
            regular_season_end=d.get("regularSeasonEndDate"),
            post_season_start=d.get("postSeasonStartDate"),
            post_season_end=d.get("postSeasonEndDate"),
            season_end=d.get("seasonEndDate"),
            raw=d,
        )


@dataclass
class League:
    id: int
    name: str
    abbreviation: str
    name_short: str
    season: Optional[str]
    num_teams: int
    num_games: int
    has_wild_card: bool
    active: bool
    season_dates: Optional[SeasonDates]
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "League":
        sd = d.get("seasonDateInfo")
        return cls(
            id=d["id"],
            name=d["name"],
            abbreviation=d.get("abbreviation", ""),
            name_short=d.get("nameShort", ""),
            season=d.get("season"),
            num_teams=d.get("numTeams", 0),
            num_games=d.get("numGames", 0),
            has_wild_card=d.get("hasWildCard", False),
            active=d.get("active", True),
            season_dates=SeasonDates._from_dict(sd) if sd else None,
            raw=d,
        )


class LeaguesEndpoint:
    AL = AL
    NL = NL

    def __init__(self, http: "HTTPClient"):
        self._http = http

    def list(
        self,
        sport_id: int = 1,
        season: Optional[int] = None,
        league_ids: Optional[list[int]] = None,
    ) -> list[League]:
        """List leagues. Defaults to MLB (sport_id=1)."""
        params: dict = {"sportId": sport_id}
        if season:
            params["season"] = season
        if league_ids:
            params["leagueIds"] = ",".join(str(i) for i in league_ids)
        data = self._http.get("leagues", **params)
        return [League._from_dict(l) for l in data.get("leagues", [])]

    def get(self, league_id: int, season: Optional[int] = None) -> League:
        """Return a single league by ID."""
        params: dict = {}
        if season:
            params["season"] = season
        data = self._http.get(f"leagues/{league_id}", **params)
        leagues = data.get("leagues", [])
        if not leagues:
            from ..exceptions import MLBNotFoundError
            raise MLBNotFoundError(404, f"League {league_id} not found")
        return League._from_dict(leagues[0])
