"""Integration tests for TeamsEndpoint."""
import pytest
from mlb import MLBClient
from mlb.endpoints.teams import Team, RosterEntry


@pytest.fixture(scope="module")
def client():
    return MLBClient()


def test_teams_list(client):
    teams = client.teams.list()
    assert len(teams) == 30
    assert all(isinstance(t, Team) for t in teams)


def test_team_fields(client):
    teams = client.teams.list()
    t = teams[0]
    assert t.id > 0
    assert t.name
    assert t.abbreviation
    assert t.league_id in (103, 104)


def test_team_get(client):
    dodgers = client.teams.get(119)
    assert dodgers.id == 119
    assert "Dodgers" in dodgers.name
    assert dodgers.location_name == "Los Angeles"


def test_team_not_found(client):
    from mlb import MLBNotFoundError
    with pytest.raises(MLBNotFoundError):
        client.teams.get(99999)


def test_team_roster_active(client):
    roster = client.teams.roster(119)
    assert len(roster) > 0
    assert all(isinstance(r, RosterEntry) for r in roster)
    for r in roster:
        assert r.person_id > 0
        assert r.person_name
        assert r.position_code


def test_team_roster_40man(client):
    # The 40-man can temporarily exceed 40 due to IL placements
    roster = client.teams.roster(119, roster_type="40Man")
    assert 25 <= len(roster) <= 50


def test_teams_by_division(client):
    from mlb.endpoints.divisions import DivisionsEndpoint
    nl_west = client.teams.list(division_id=DivisionsEndpoint.NL_WEST)
    assert len(nl_west) == 5
    team_ids = {t.id for t in nl_west}
    assert 119 in team_ids  # Dodgers


def test_team_stats(client):
    stats = client.teams.stats(119, stat_type="season", groups=["hitting"])
    assert isinstance(stats, dict)
