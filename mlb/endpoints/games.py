from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .._http import HTTPClient


@dataclass
class LinescoreInning:
    num: int
    ordinal: str
    away_runs: Optional[int]
    home_runs: Optional[int]
    away_hits: Optional[int]
    home_hits: Optional[int]
    away_errors: Optional[int]
    home_errors: Optional[int]
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "LinescoreInning":
        away = d.get("away", {})
        home = d.get("home", {})
        return cls(
            num=d.get("num", 0),
            ordinal=d.get("ordinalNum", ""),
            away_runs=away.get("runs"),
            home_runs=home.get("runs"),
            away_hits=away.get("hits"),
            home_hits=home.get("hits"),
            away_errors=away.get("errors"),
            home_errors=home.get("errors"),
            raw=d,
        )


@dataclass
class LinescoreTotals:
    runs: int
    hits: int
    errors: int
    left_on_base: int

    @classmethod
    def _from_dict(cls, d: dict) -> "LinescoreTotals":
        return cls(
            runs=d.get("runs", 0),
            hits=d.get("hits", 0),
            errors=d.get("errors", 0),
            left_on_base=d.get("leftOnBase", 0),
        )


@dataclass
class Linescore:
    current_inning: Optional[int]
    current_inning_ordinal: Optional[str]
    inning_state: Optional[str]
    inning_half: Optional[str]
    is_top_inning: Optional[bool]
    scheduled_innings: int
    innings: list[LinescoreInning]
    away: LinescoreTotals
    home: LinescoreTotals
    balls: int
    strikes: int
    outs: int
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "Linescore":
        return cls(
            current_inning=d.get("currentInning"),
            current_inning_ordinal=d.get("currentInningOrdinal"),
            inning_state=d.get("inningState"),
            inning_half=d.get("inningHalf"),
            is_top_inning=d.get("isTopInning"),
            scheduled_innings=d.get("scheduledInnings", 9),
            innings=[LinescoreInning._from_dict(i) for i in d.get("innings", [])],
            away=LinescoreTotals._from_dict(d.get("teams", {}).get("away", {})),
            home=LinescoreTotals._from_dict(d.get("teams", {}).get("home", {})),
            balls=d.get("balls", 0),
            strikes=d.get("strikes", 0),
            outs=d.get("outs", 0),
            raw=d,
        )


@dataclass
class Weather:
    condition: Optional[str]
    temp: Optional[str]
    wind: Optional[str]

    @classmethod
    def _from_dict(cls, d: dict) -> "Weather":
        return cls(
            condition=d.get("condition"),
            temp=d.get("temp"),
            wind=d.get("wind"),
        )


@dataclass
class GameInfo:
    attendance: Optional[int]
    first_pitch: Optional[str]
    duration_minutes: Optional[int]

    @classmethod
    def _from_dict(cls, d: dict) -> "GameInfo":
        return cls(
            attendance=d.get("attendance"),
            first_pitch=d.get("firstPitch"),
            duration_minutes=d.get("gameDurationMinutes"),
        )


@dataclass
class LiveFeed:
    game_pk: int
    game_type: str
    season: str
    game_date: str
    status_code: str
    status_detail: str
    abstract_state: str
    away_team_id: int
    away_team_name: str
    home_team_id: int
    home_team_name: str
    venue_id: Optional[int]
    venue_name: Optional[str]
    weather: Optional[Weather]
    game_info: Optional[GameInfo]
    linescore: Optional[Linescore]
    probable_pitcher_away: Optional[dict]
    probable_pitcher_home: Optional[dict]
    decisions: Optional[dict]
    flags: dict
    raw: dict

    @classmethod
    def _from_dict(cls, d: dict) -> "LiveFeed":
        gd = d.get("gameData", {})
        ld = d.get("liveData", {})
        game = gd.get("game", {})
        status = gd.get("status", {})
        teams = gd.get("teams", {})
        away = teams.get("away", {})
        home = teams.get("home", {})
        venue = gd.get("venue", {})
        weather = gd.get("weather")
        game_info = gd.get("gameInfo")
        pitchers = gd.get("probablePitchers", {})
        linescore = ld.get("linescore")
        decisions = ld.get("decisions")
        return cls(
            game_pk=d.get("gamePk", 0),
            game_type=game.get("type", ""),
            season=game.get("season", ""),
            game_date=gd.get("datetime", {}).get("dateTime", ""),
            status_code=status.get("statusCode", ""),
            status_detail=status.get("detailedState", ""),
            abstract_state=status.get("abstractGameState", ""),
            away_team_id=away.get("id", 0),
            away_team_name=away.get("name", ""),
            home_team_id=home.get("id", 0),
            home_team_name=home.get("name", ""),
            venue_id=venue.get("id"),
            venue_name=venue.get("name"),
            weather=Weather._from_dict(weather) if weather else None,
            game_info=GameInfo._from_dict(game_info) if game_info else None,
            linescore=Linescore._from_dict(linescore) if linescore else None,
            probable_pitcher_away=pitchers.get("away"),
            probable_pitcher_home=pitchers.get("home"),
            decisions=decisions,
            flags=gd.get("flags", {}),
            raw=d,
        )

    @property
    def is_no_hitter(self) -> bool:
        return self.flags.get("noHitter", False)

    @property
    def is_perfect_game(self) -> bool:
        return self.flags.get("perfectGame", False)


class GamesEndpoint:
    def __init__(self, http: "HTTPClient"):
        self._http = http

    def live_feed(self, game_pk: int, time_code: Optional[str] = None) -> LiveFeed:
        """
        Return the full live feed for a game (v1.1 endpoint).

        time_code: replay at a specific timestamp (YYYYMMDD_HHMMSS format)
        """
        params: dict = {}
        if time_code:
            params["timecode"] = time_code
        data = self._http.get(f"game/{game_pk}/feed/live", api_version="v1.1", **params)
        return LiveFeed._from_dict(data)

    def linescore(self, game_pk: int) -> Linescore:
        """Return just the linescore for a game."""
        data = self._http.get(f"game/{game_pk}/linescore")
        return Linescore._from_dict(data)

    def boxscore(self, game_pk: int) -> dict:
        """
        Return the full boxscore for a game.

        Returns the raw dict — the boxscore structure is complex enough that
        a full model would be unwieldy. Access `.raw` directly.
        """
        return self._http.get(f"game/{game_pk}/boxscore")

    def play_by_play(self, game_pk: int) -> dict:
        """Return all plays for a game (raw dict)."""
        data = self._http.get(f"game/{game_pk}/feed/live", api_version="v1.1")
        return data.get("liveData", {}).get("plays", {})

    def content(self, game_pk: int) -> dict:
        """Return editorial content, highlights, and media for a game."""
        return self._http.get(f"game/{game_pk}/content")

    def diff_patch(self, game_pk: int, start_time: str, end_time: str) -> dict:
        """
        Return only the changed fields between two timestamps (efficient polling).

        start_time, end_time: YYYYMMDD_HHMMSS format
        """
        return self._http.get(
            f"game/{game_pk}/feed/live/diffPatch",
            api_version="v1.1",
            startTimecode=start_time,
            endTimecode=end_time,
        )
