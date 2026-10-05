from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .._http import HTTPClient


@dataclass
class Streak:
    code: str
    type: str
    number: int

    @classmethod
    def _from_dict(cls, d: dict) -> "Streak":
        return cls(
            code=d.get("streakCode", ""),
            type=d.get("streakType", ""),
            number=d.get("streakNumber", 0),
        )


@dataclass
class LeagueRecord:
    wins: int
    losses: int
    ties: int
    pct: str

    @classmethod
    def _from_dict(cls, d: dict) -> "LeagueRecord":
        return cls(
            wins=d.get("wins", 0),
            losses=d.get("losses", 0),
            ties=d.get("ties", 0),
            pct=d.get("pct", ".000"),
        )


@dataclass
class TeamRecord:
    team_id: int
    team_name: str
    season: str
    division_rank: str
    league_rank: str
    sport_rank: str
    games_played: int
    games_back: str
    wild_card_games_back: str
    wins: int
    losses: int
    run_differential: int
    winning_pct: str
    streak: Optional[Streak]
    league_record: LeagueRecord
    division_champ: bool
    division_leader: bool
    wild_card_leader: bool
    has_wildcard: bool
    clinched: bool
    elimination_number: Optional[str]
    wild_card_elimination_number: Optional[str]
    runs_scored: int
    runs_allowed: int
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "TeamRecord":
        team = d.get("team", {})
        streak = d.get("streak")
        return cls(
            team_id=team.get("id", 0),
            team_name=team.get("name", ""),
            season=d.get("season", ""),
            division_rank=d.get("divisionRank", ""),
            league_rank=d.get("leagueRank", ""),
            sport_rank=d.get("sportRank", ""),
            games_played=d.get("gamesPlayed", 0),
            games_back=d.get("gamesBack", "-"),
            wild_card_games_back=d.get("wildCardGamesBack", "-"),
            wins=d.get("wins", 0),
            losses=d.get("losses", 0),
            run_differential=d.get("runDifferential", 0),
            winning_pct=d.get("winningPercentage", ".000"),
            streak=Streak._from_dict(streak) if streak else None,
            league_record=LeagueRecord._from_dict(d.get("leagueRecord", {})),
            division_champ=d.get("divisionChamp", False),
            division_leader=d.get("divisionLeader", False),
            wild_card_leader=d.get("wildCardLeader", False),
            has_wildcard=d.get("hasWildcard", False),
            clinched=d.get("clinched", False),
            elimination_number=d.get("eliminationNumber"),
            wild_card_elimination_number=d.get("wildCardEliminationNumber"),
            runs_scored=d.get("runsScored", 0),
            runs_allowed=d.get("runsAllowed", 0),
            raw=d,
        )


@dataclass
class DivisionStandings:
    standings_type: str
    league_id: Optional[int]
    division_id: Optional[int]
    last_updated: Optional[str]
    team_records: list[TeamRecord]
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "DivisionStandings":
        return cls(
            standings_type=d.get("standingsType", ""),
            league_id=d.get("league", {}).get("id"),
            division_id=d.get("division", {}).get("id"),
            last_updated=d.get("lastUpdated"),
            team_records=[TeamRecord._from_dict(tr) for tr in d.get("teamRecords", [])],
            raw=d,
        )


class StandingsEndpoint:
    def __init__(self, http: "HTTPClient"):
        self._http = http

    def get(
        self,
        league_ids: Optional[list[int]] = None,
        season: Optional[int] = None,
        standings_type: str = "regularSeason",
        date: Optional[str] = None,
        hydrate: Optional[list[str]] = None,
    ) -> list[DivisionStandings]:
        """
        Fetch standings.

        league_ids: defaults to [103, 104] (AL + NL)
        standings_type: "regularSeason", "wildCard", "divisionLeaders",
                        "firstHalf", "secondHalf", "springTraining", "postseason"
        date: standings as of a specific date (YYYY-MM-DD)
        """
        if league_ids is None:
            league_ids = [103, 104]

        params: dict = {
            "leagueId": ",".join(str(i) for i in league_ids),
            "standingsTypes": standings_type,
        }
        if season:
            params["season"] = season
        if date:
            params["date"] = date
        if hydrate:
            params["hydrate"] = ",".join(hydrate)

        data = self._http.get("standings", **params)
        return [DivisionStandings._from_dict(r) for r in data.get("records", [])]

    def wild_card(self, season: Optional[int] = None) -> list[DivisionStandings]:
        """Wild card standings."""
        return self.get(standings_type="wildCard", season=season)

    def as_of(self, date: str, season: Optional[int] = None) -> list[DivisionStandings]:
        """Standings as of a specific date (YYYY-MM-DD)."""
        return self.get(date=date, season=season)
