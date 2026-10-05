from __future__ import annotations

from typing import Optional

from ._http import HTTPClient
from .endpoints.divisions import DivisionsEndpoint
from .endpoints.games import GamesEndpoint
from .endpoints.leagues import LeaguesEndpoint
from .endpoints.players import PlayersEndpoint
from .endpoints.schedule import ScheduleEndpoint
from .endpoints.sports import SportsEndpoint
from .endpoints.standings import StandingsEndpoint
from .endpoints.teams import TeamsEndpoint
from .endpoints.venues import VenuesEndpoint


class MLBClient:
    """
    Python client for the MLB Stats API (statsapi.mlb.com).

    Usage::

        from mlb import MLBClient

        client = MLBClient()
        games = client.schedule.today()
        teams = client.teams.list()
        player = client.players.get(660271)  # Shohei Ohtani

    All endpoints are accessible as attributes on the client:
        client.schedule, client.teams, client.players, client.games,
        client.standings, client.leagues, client.divisions,
        client.venues, client.sports
    """

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit_delay: float = 0.0,
    ):
        """
        Create an MLB API client.

        Args:
            timeout: HTTP request timeout in seconds (default 30)
            max_retries: Number of retries on 5xx errors (default 3)
            rate_limit_delay: Minimum seconds between requests (default 0 = no delay).
                              Set to ~0.1 for polite scraping of many requests.
        """
        self._http = HTTPClient(
            timeout=timeout,
            max_retries=max_retries,
            rate_limit_delay=rate_limit_delay,
        )
        self.schedule = ScheduleEndpoint(self._http)
        self.teams = TeamsEndpoint(self._http)
        self.players = PlayersEndpoint(self._http)
        self.games = GamesEndpoint(self._http)
        self.standings = StandingsEndpoint(self._http)
        self.leagues = LeaguesEndpoint(self._http)
        self.divisions = DivisionsEndpoint(self._http)
        self.venues = VenuesEndpoint(self._http)
        self.sports = SportsEndpoint(self._http)
