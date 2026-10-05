"""Integration tests for StandingsEndpoint."""
import pytest
from mlb import MLBClient
from mlb.endpoints.standings import DivisionStandings, TeamRecord


@pytest.fixture(scope="module")
def client():
    return MLBClient()


def test_standings_default(client):
    standings = client.standings.get()
    assert len(standings) == 6  # 6 divisions
    assert all(isinstance(s, DivisionStandings) for s in standings)


def test_standings_have_teams(client):
    standings = client.standings.get()
    for div in standings:
        assert len(div.team_records) == 5
        assert all(isinstance(tr, TeamRecord) for tr in div.team_records)


def test_team_record_fields(client):
    standings = client.standings.get()
    tr = standings[0].team_records[0]
    assert tr.team_id > 0
    assert tr.team_name
    assert tr.wins >= 0
    assert tr.losses >= 0
    assert tr.games_played == tr.wins + tr.losses
    assert tr.division_rank in ("1", "2", "3", "4", "5")


def test_standings_al_only(client):
    al_standings = client.standings.get(league_ids=[103])
    assert len(al_standings) == 3  # AL East, Central, West
    for div in al_standings:
        assert div.league_id == 103


def test_standings_wild_card(client):
    wc = client.standings.wild_card()
    assert len(wc) > 0


@pytest.mark.xfail(reason="standings?date= consistently 500s on the MLB API (known upstream bug)")
def test_standings_as_of_date(client):
    standings = client.standings.as_of("2026-07-15")
    assert len(standings) == 6
    for div in standings:
        for tr in div.team_records:
            assert tr.games_played < 100


def test_standings_season(client):
    standings = client.standings.get(season=2026)
    assert len(standings) == 6
    for div in standings:
        for tr in div.team_records:
            assert tr.games_played > 100  # Full season
