from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .._http import HTTPClient


@dataclass
class Position:
    code: str
    name: str
    type: str
    abbreviation: str

    @classmethod
    def _from_dict(cls, d: dict) -> "Position":
        return cls(
            code=d.get("code", ""),
            name=d.get("name", ""),
            type=d.get("type", ""),
            abbreviation=d.get("abbreviation", ""),
        )


@dataclass
class Hand:
    code: str
    description: str

    @classmethod
    def _from_dict(cls, d: dict) -> "Hand":
        return cls(code=d.get("code", ""), description=d.get("description", ""))


@dataclass
class Player:
    id: int
    full_name: str
    first_name: str
    last_name: str
    use_name: str
    primary_number: Optional[str]
    birth_date: Optional[str]
    current_age: Optional[int]
    birth_city: Optional[str]
    birth_country: Optional[str]
    height: Optional[str]
    weight: Optional[int]
    active: bool
    primary_position: Optional[Position]
    mlb_debut_date: Optional[str]
    bat_side: Optional[Hand]
    pitch_hand: Optional[Hand]
    strike_zone_top: Optional[float]
    strike_zone_bottom: Optional[float]
    name_slug: Optional[str]
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "Player":
        pos = d.get("primaryPosition")
        bat = d.get("batSide")
        pitch = d.get("pitchHand")
        return cls(
            id=d["id"],
            full_name=d.get("fullName", ""),
            first_name=d.get("firstName", ""),
            last_name=d.get("lastName", ""),
            use_name=d.get("useName", ""),
            primary_number=d.get("primaryNumber"),
            birth_date=d.get("birthDate"),
            current_age=d.get("currentAge"),
            birth_city=d.get("birthCity"),
            birth_country=d.get("birthCountry"),
            height=d.get("height"),
            weight=d.get("weight"),
            active=d.get("active", True),
            primary_position=Position._from_dict(pos) if pos else None,
            mlb_debut_date=d.get("mlbDebutDate"),
            bat_side=Hand._from_dict(bat) if bat else None,
            pitch_hand=Hand._from_dict(pitch) if pitch else None,
            strike_zone_top=d.get("strikeZoneTop"),
            strike_zone_bottom=d.get("strikeZoneBottom"),
            name_slug=d.get("nameSlug"),
            raw=d,
        )


@dataclass
class StatSplit:
    season: Optional[str]
    game_type: Optional[str]
    stat: dict
    team: Optional[dict]
    player: Optional[dict]
    position: Optional[dict]
    league: Optional[dict]
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "StatSplit":
        return cls(
            season=d.get("season"),
            game_type=d.get("gameType"),
            stat=d.get("stat", {}),
            team=d.get("team"),
            player=d.get("player"),
            position=d.get("position"),
            league=d.get("league"),
            raw=d,
        )


@dataclass
class StatGroup:
    group: str
    type: str
    splits: list[StatSplit]
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "StatGroup":
        return cls(
            group=d.get("group", {}).get("displayName", ""),
            type=d.get("type", {}).get("displayName", ""),
            splits=[StatSplit._from_dict(s) for s in d.get("splits", [])],
            raw=d,
        )


class PlayersEndpoint:
    def __init__(self, http: "HTTPClient"):
        self._http = http

    def get(self, player_id: int, season: Optional[int] = None) -> Player:
        """Return a single player by MLB player ID."""
        params: dict = {}
        if season:
            params["season"] = season
        data = self._http.get(f"people/{player_id}", **params)
        people = data.get("people", [])
        if not people:
            from ..exceptions import MLBNotFoundError
            raise MLBNotFoundError(404, f"Player {player_id} not found")
        return Player._from_dict(people[0])

    def get_many(self, player_ids: list[int], season: Optional[int] = None) -> list[Player]:
        """Fetch multiple players in a single request."""
        params: dict = {"personIds": ",".join(str(i) for i in player_ids)}
        if season:
            params["season"] = season
        data = self._http.get("people", **params)
        return [Player._from_dict(p) for p in data.get("people", [])]

    def search(self, name: str, sport_id: int = 1, active: Optional[bool] = None) -> list[Player]:
        """
        Search for players by name.

        Uses the /people/search endpoint; returns partial matches.
        """
        params: dict = {"names": name, "sportId": sport_id}
        if active is not None:
            params["active"] = str(active).lower()
        data = self._http.get("people/search", **params)
        return [Player._from_dict(p) for p in data.get("people", [])]

    def stats(
        self,
        player_id: int,
        groups: Optional[list[str]] = None,
        stat_type: str = "season",
        season: Optional[int] = None,
        game_type: str = "R",
    ) -> list[StatGroup]:
        """
        Return player stats.

        groups: ["hitting", "pitching", "fielding"] — defaults to all three
        stat_type: "season", "yearByYear", "career", "gameLog", "lastXGames",
                   "byDateRange", "vsPlayer", "vsTeam"
        game_type: "R" (regular), "P" (postseason), "S" (spring), "A" (allstar)
        """
        if groups is None:
            groups = ["hitting", "pitching", "fielding"]

        params: dict = {
            "stats": stat_type,
            "group": ",".join(groups),
            "gameType": game_type,
        }
        if season:
            params["season"] = season

        data = self._http.get(f"people/{player_id}/stats", **params)
        return [StatGroup._from_dict(s) for s in data.get("stats", [])]

    def current_game_stats(self, player_id: int) -> list[StatGroup]:
        """Stats for the player's most recent game."""
        return self.stats(player_id, stat_type="lastXGames")

    def career_stats(self, player_id: int, groups: Optional[list[str]] = None) -> list[StatGroup]:
        """Career cumulative stats."""
        return self.stats(player_id, stat_type="career", groups=groups)

    def year_by_year(self, player_id: int, groups: Optional[list[str]] = None) -> list[StatGroup]:
        """Stats broken down by season."""
        return self.stats(player_id, stat_type="yearByYear", groups=groups)
