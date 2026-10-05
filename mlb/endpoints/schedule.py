from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from .._http import HTTPClient

DateLike = Union[str, date, datetime]


def _fmt_date(d: DateLike) -> str:
    if isinstance(d, (date, datetime)):
        return d.strftime("%Y-%m-%d")
    return d


@dataclass
class GameStatus:
    abstract_state: str
    coded_state: str
    detailed_state: str
    status_code: str
    start_time_tbd: bool

    @classmethod
    def _from_dict(cls, d: dict) -> "GameStatus":
        return cls(
            abstract_state=d.get("abstractGameState", ""),
            coded_state=d.get("codedGameState", ""),
            detailed_state=d.get("detailedState", ""),
            status_code=d.get("statusCode", ""),
            start_time_tbd=d.get("startTimeTBD", False),
        )

    @property
    def is_final(self) -> bool:
        return self.abstract_state == "Final"

    @property
    def is_live(self) -> bool:
        return self.abstract_state == "Live"

    @property
    def is_preview(self) -> bool:
        return self.abstract_state == "Preview"


@dataclass
class ScheduleTeam:
    team_id: int
    team_name: str
    score: Optional[int]
    wins: int
    losses: int
    win_pct: str
    is_winner: Optional[bool]
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "ScheduleTeam":
        team = d.get("team", {})
        record = d.get("leagueRecord", {})
        return cls(
            team_id=team.get("id", 0),
            team_name=team.get("name", ""),
            score=d.get("score"),
            wins=record.get("wins", 0),
            losses=record.get("losses", 0),
            win_pct=record.get("pct", ".000"),
            is_winner=d.get("isWinner"),
            raw=d,
        )


@dataclass
class ScheduledGame:
    game_pk: int
    game_guid: str
    game_type: str
    season: str
    game_date: str
    official_date: str
    status: GameStatus
    away: ScheduleTeam
    home: ScheduleTeam
    venue_id: Optional[int]
    venue_name: Optional[str]
    day_night: str
    scheduled_innings: int
    games_in_series: int
    series_game_number: int
    series_description: str
    double_header: str
    game_number: int
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "ScheduledGame":
        teams = d.get("teams", {})
        venue = d.get("venue", {})
        return cls(
            game_pk=d["gamePk"],
            game_guid=d.get("gameGuid", ""),
            game_type=d.get("gameType", ""),
            season=d.get("season", ""),
            game_date=d.get("gameDate", ""),
            official_date=d.get("officialDate", ""),
            status=GameStatus._from_dict(d.get("status", {})),
            away=ScheduleTeam._from_dict(teams.get("away", {})),
            home=ScheduleTeam._from_dict(teams.get("home", {})),
            venue_id=venue.get("id"),
            venue_name=venue.get("name"),
            day_night=d.get("dayNight", ""),
            scheduled_innings=d.get("scheduledInnings", 9),
            games_in_series=d.get("gamesInSeries", 1),
            series_game_number=d.get("seriesGameNumber", 1),
            series_description=d.get("seriesDescription", ""),
            double_header=d.get("doubleHeader", "N"),
            game_number=d.get("gameNumber", 1),
            raw=d,
        )

    @property
    def is_double_header(self) -> bool:
        return self.double_header != "N"


@dataclass
class ScheduleDate:
    date: str
    total_games: int
    total_games_in_progress: int
    games: list[ScheduledGame]
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "ScheduleDate":
        return cls(
            date=d["date"],
            total_games=d.get("totalGames", 0),
            total_games_in_progress=d.get("totalGamesInProgress", 0),
            games=[ScheduledGame._from_dict(g) for g in d.get("games", [])],
            raw=d,
        )


@dataclass
class Schedule:
    total_items: int
    total_games: int
    total_games_in_progress: int
    dates: list[ScheduleDate]
    raw: dict

    @property
    def games(self) -> list[ScheduledGame]:
        """Flat list of all games across all dates."""
        return [g for sd in self.dates for g in sd.games]

    @classmethod
    def _from_dict(cls, d: dict) -> "Schedule":
        return cls(
            total_items=d.get("totalItems", 0),
            total_games=d.get("totalGames", 0),
            total_games_in_progress=d.get("totalGamesInProgress", 0),
            dates=[ScheduleDate._from_dict(dt) for dt in d.get("dates", [])],
            raw=d,
        )


class ScheduleEndpoint:
    def __init__(self, http: "HTTPClient"):
        self._http = http

    def get(
        self,
        date: Optional[DateLike] = None,
        start_date: Optional[DateLike] = None,
        end_date: Optional[DateLike] = None,
        team_id: Optional[int] = None,
        sport_id: int = 1,
        game_type: Optional[str] = None,
        season: Optional[int] = None,
        hydrate: Optional[list[str]] = None,
    ) -> Schedule:
        """
        Fetch the game schedule.

        Provide either `date` (single day) or `start_date`/`end_date` (range).
        If neither is provided, returns today's schedule.

        game_type: "R" (regular), "P" (postseason), "S" (spring), "A" (all-star),
                   "F" (wild card), "D" (division series), "L" (LCS), "W" (World Series)
        hydrate: e.g. ["linescore", "team", "venue", "decisions", "probablePitcher"]
        """
        params: dict = {"sportId": sport_id}
        if date:
            params["date"] = _fmt_date(date)
        if start_date:
            params["startDate"] = _fmt_date(start_date)
        if end_date:
            params["endDate"] = _fmt_date(end_date)
        if team_id:
            params["teamId"] = team_id
        if game_type:
            params["gameType"] = game_type
        if season:
            params["season"] = season
        if hydrate:
            params["hydrate"] = ",".join(hydrate)

        data = self._http.get("schedule", **params)
        return Schedule._from_dict(data)

    def today(self, sport_id: int = 1, hydrate: Optional[list[str]] = None) -> Schedule:
        """Today's schedule."""
        return self.get(sport_id=sport_id, hydrate=hydrate)

    def for_team(
        self,
        team_id: int,
        season: Optional[int] = None,
        game_type: str = "R",
    ) -> Schedule:
        """Full season schedule for a specific team."""
        return self.get(team_id=team_id, season=season, game_type=game_type)
