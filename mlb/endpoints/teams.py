from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .._http import HTTPClient


@dataclass
class Team:
    id: int
    name: str
    abbreviation: str
    team_name: str
    location_name: str
    short_name: str
    franchise_name: str
    club_name: str
    team_code: str
    file_code: str
    season: Optional[int]
    first_year_of_play: Optional[str]
    venue_id: Optional[int]
    venue_name: Optional[str]
    league_id: Optional[int]
    league_name: Optional[str]
    division_id: Optional[int]
    division_name: Optional[str]
    sport_id: Optional[int]
    active: bool
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "Team":
        return cls(
            id=d["id"],
            name=d["name"],
            abbreviation=d.get("abbreviation", ""),
            team_name=d.get("teamName", ""),
            location_name=d.get("locationName", ""),
            short_name=d.get("shortName", ""),
            franchise_name=d.get("franchiseName", ""),
            club_name=d.get("clubName", ""),
            team_code=d.get("teamCode", ""),
            file_code=d.get("fileCode", ""),
            season=d.get("season"),
            first_year_of_play=d.get("firstYearOfPlay"),
            venue_id=d.get("venue", {}).get("id"),
            venue_name=d.get("venue", {}).get("name"),
            league_id=d.get("league", {}).get("id"),
            league_name=d.get("league", {}).get("name"),
            division_id=d.get("division", {}).get("id"),
            division_name=d.get("division", {}).get("name"),
            sport_id=d.get("sport", {}).get("id"),
            active=d.get("active", True),
            raw=d,
        )


@dataclass
class RosterEntry:
    person_id: int
    person_name: str
    jersey_number: Optional[str]
    position_code: str
    position_name: str
    position_type: str
    position_abbreviation: str
    status: str
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "RosterEntry":
        person = d.get("person", {})
        position = d.get("position", {})
        status = d.get("status", {})
        return cls(
            person_id=person.get("id", 0),
            person_name=person.get("fullName", ""),
            jersey_number=d.get("jerseyNumber"),
            position_code=position.get("code", ""),
            position_name=position.get("name", ""),
            position_type=position.get("type", ""),
            position_abbreviation=position.get("abbreviation", ""),
            status=status.get("description", ""),
            raw=d,
        )


class TeamsEndpoint:
    # Well-known team IDs
    ANGELS = 108
    ASTROS = 117
    ATHLETICS = 133
    BLUE_JAYS = 141
    BRAVES = 144
    BREWERS = 158
    CARDINALS = 138
    CUBS = 112
    DIAMONDBACKS = 109
    DODGERS = 119
    GIANTS = 137
    GUARDIANS = 114
    MARINERS = 136
    MARLINS = 146
    METS = 121
    NATIONALS = 120
    ORIOLES = 110
    PADRES = 135
    PHILLIES = 143
    PIRATES = 134
    RANGERS = 140
    RAYS = 139
    RED_SOX = 111
    REDS = 113
    ROCKIES = 115
    ROYALS = 118
    TIGERS = 116
    TWINS = 142
    WHITE_SOX = 145
    YANKEES = 147

    def __init__(self, http: "HTTPClient"):
        self._http = http

    def list(
        self,
        sport_id: int = 1,
        season: Optional[int] = None,
        league_id: Optional[int] = None,
        division_id: Optional[int] = None,
        active_status: Optional[str] = None,
    ) -> list[Team]:
        """List all teams. Defaults to active MLB teams.

        Note: division_id is filtered client-side — the API ignores that parameter.
        """
        params: dict = {"sportId": sport_id}
        if season:
            params["season"] = season
        if league_id:
            params["leagueId"] = league_id
        if active_status:
            params["activeStatus"] = active_status
        data = self._http.get("teams", **params)
        teams = [Team._from_dict(t) for t in data.get("teams", [])]
        if division_id is not None:
            teams = [t for t in teams if t.division_id == division_id]
        return teams

    def get(self, team_id: int, season: Optional[int] = None) -> Team:
        """Return a single team by ID."""
        params: dict = {}
        if season:
            params["season"] = season
        data = self._http.get(f"teams/{team_id}", **params)
        teams = data.get("teams", [])
        if not teams:
            from ..exceptions import MLBNotFoundError
            raise MLBNotFoundError(404, f"Team {team_id} not found")
        return Team._from_dict(teams[0])

    def roster(
        self,
        team_id: int,
        roster_type: str = "active",
        season: Optional[int] = None,
        date: Optional[str] = None,
    ) -> list[RosterEntry]:
        """
        Fetch a team's roster.

        roster_type options: "active", "fullRoster", "40Man", "depthChart",
                             "gameday", "nonRosterInvitees"
        """
        params: dict = {"rosterType": roster_type}
        if season:
            params["season"] = season
        if date:
            params["date"] = date
        data = self._http.get(f"teams/{team_id}/roster", **params)
        return [RosterEntry._from_dict(r) for r in data.get("roster", [])]

    def coaches(self, team_id: int, season: Optional[int] = None) -> list[dict]:
        """Return the coaching staff for a team."""
        params: dict = {}
        if season:
            params["season"] = season
        data = self._http.get(f"teams/{team_id}/coaches", **params)
        return data.get("roster", [])

    def stats(
        self,
        team_id: int,
        stat_type: str = "season",
        groups: Optional[list[str]] = None,
        season: Optional[int] = None,
    ) -> dict:
        """Return team stats. Returns raw dict — structure varies by group/type."""
        params: dict = {"stats": stat_type}
        if groups:
            params["group"] = ",".join(groups)
        if season:
            params["season"] = season
        return self._http.get(f"teams/{team_id}/stats", **params)
