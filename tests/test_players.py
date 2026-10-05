"""Integration tests for PlayersEndpoint."""
import pytest
from mlb import MLBClient
from mlb.endpoints.players import Player, StatGroup, StatSplit

OHTANI_ID = 660271
JUDGE_ID = 592450


@pytest.fixture(scope="module")
def client():
    return MLBClient()


def test_player_get(client):
    player = client.players.get(OHTANI_ID)
    assert isinstance(player, Player)
    assert player.id == OHTANI_ID
    assert "Ohtani" in player.full_name
    assert player.active is True


def test_player_fields(client):
    player = client.players.get(OHTANI_ID)
    assert player.first_name
    assert player.last_name
    assert player.birth_date
    assert player.birth_country == "Japan"
    assert player.height
    assert player.weight
    assert player.primary_position is not None
    assert player.bat_side is not None
    assert player.pitch_hand is not None


def test_player_not_found(client):
    from mlb import MLBNotFoundError
    with pytest.raises(MLBNotFoundError):
        client.players.get(9999999)


def test_player_get_many(client):
    players = client.players.get_many([OHTANI_ID, JUDGE_ID])
    assert len(players) == 2
    ids = {p.id for p in players}
    assert OHTANI_ID in ids
    assert JUDGE_ID in ids


def test_player_search(client):
    results = client.players.search("ohtani")
    assert len(results) > 0
    names = [p.full_name.lower() for p in results]
    assert any("ohtani" in n for n in names)


def test_player_stats_season(client):
    stats = client.players.stats(OHTANI_ID, groups=["hitting"], stat_type="season", season=2026)
    assert isinstance(stats, list)
    assert len(stats) > 0
    assert all(isinstance(sg, StatGroup) for sg in stats)


def test_player_stats_splits(client):
    stats = client.players.stats(OHTANI_ID, groups=["hitting"], stat_type="yearByYear")
    for sg in stats:
        assert isinstance(sg.splits, list)
        for split in sg.splits:
            assert isinstance(split, StatSplit)
            assert isinstance(split.stat, dict)


def test_player_career_stats(client):
    stats = client.players.career_stats(JUDGE_ID, groups=["hitting"])
    assert len(stats) > 0


def test_player_year_by_year(client):
    stats = client.players.year_by_year(OHTANI_ID, groups=["hitting"])
    seasons = [s.season for sg in stats for s in sg.splits]
    assert len(seasons) > 3  # Ohtani has been in MLB since 2018
