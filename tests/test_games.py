"""Integration tests for GamesEndpoint."""
import pytest
from mlb import MLBClient
from mlb.endpoints.games import LiveFeed, Linescore

# A completed 2026 regular-season game: Tampa Bay Rays 4 @ New York Yankees 6, 2026-09-24
COMPLETED_GAME_PK = 823493


@pytest.fixture(scope="module")
def client():
    return MLBClient()


@pytest.fixture(scope="module")
def completed_game_pk(client):
    """Find a completed game from a known recent date."""
    sched = client.schedule.get(date="2026-04-20")
    for g in sched.games:
        if g.status.is_final:
            return g.game_pk
    pytest.skip("No completed games found on 2026-04-20")


def test_live_feed(client, completed_game_pk):
    feed = client.games.live_feed(completed_game_pk)
    assert isinstance(feed, LiveFeed)
    assert feed.game_pk == completed_game_pk
    assert feed.away_team_id > 0
    assert feed.home_team_id > 0
    assert feed.abstract_state == "Final"


def test_live_feed_fields(client, completed_game_pk):
    feed = client.games.live_feed(completed_game_pk)
    assert feed.venue_name
    assert feed.season
    assert feed.game_type == "R"


def test_linescore(client, completed_game_pk):
    ls = client.games.linescore(completed_game_pk)
    assert isinstance(ls, Linescore)
    assert len(ls.innings) >= 9
    assert ls.away.runs >= 0
    assert ls.home.runs >= 0


def test_linescore_innings(client, completed_game_pk):
    ls = client.games.linescore(completed_game_pk)
    for inning in ls.innings:
        assert inning.num > 0
        assert inning.ordinal


def test_boxscore(client, completed_game_pk):
    bs = client.games.boxscore(completed_game_pk)
    assert isinstance(bs, dict)
    assert "teams" in bs


def test_play_by_play(client, completed_game_pk):
    plays = client.games.play_by_play(completed_game_pk)
    assert isinstance(plays, dict)
    assert "allPlays" in plays


def test_invalid_game_returns_empty_feed(client):
    # The API returns an empty-but-valid structure for unknown gamePks rather than 404.
    # gamePk in the body is 0 (not the requested ID), status is "Unknown".
    feed = client.games.live_feed(999999999)
    assert isinstance(feed, LiveFeed)
    assert feed.status_detail == "Unknown"
