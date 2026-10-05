"""Integration tests for ScheduleEndpoint — hit the real API."""
import pytest
from mlb import MLBClient
from mlb.endpoints.schedule import Schedule, ScheduledGame, GameStatus


@pytest.fixture(scope="module")
def client():
    return MLBClient()


def test_schedule_today(client):
    sched = client.schedule.today()
    assert isinstance(sched, Schedule)
    assert sched.total_games >= 0
    assert isinstance(sched.dates, list)


def test_schedule_specific_date(client):
    sched = client.schedule.get(date="2026-04-01")
    assert isinstance(sched, Schedule)


def test_schedule_date_range(client):
    sched = client.schedule.get(start_date="2026-04-01", end_date="2026-04-07")
    assert len(sched.dates) > 0
    assert all(isinstance(d.date, str) for d in sched.dates)


def test_schedule_games_flat(client):
    sched = client.schedule.get(date="2026-04-27")
    games = sched.games
    assert isinstance(games, list)
    for g in games:
        assert isinstance(g, ScheduledGame)
        assert g.game_pk > 0
        assert g.away.team_id > 0
        assert g.home.team_id > 0


def test_schedule_game_status(client):
    sched = client.schedule.get(date="2026-04-27")
    for g in sched.games:
        status = g.status
        assert isinstance(status, GameStatus)
        assert status.abstract_state in ("Preview", "Live", "Final")


def test_schedule_for_team(client):
    sched = client.schedule.for_team(team_id=119, season=2026)  # Dodgers
    assert sched.total_games > 0
    for g in sched.games:
        assert g.away.team_id == 119 or g.home.team_id == 119


def test_schedule_hydrate_linescore(client):
    sched = client.schedule.get(date="2026-04-20", hydrate=["linescore"])
    assert isinstance(sched, Schedule)
