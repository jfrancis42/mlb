"""Integration tests for leagues, divisions, venues, sports endpoints."""
import pytest
from mlb import MLBClient
from mlb.endpoints.leagues import League
from mlb.endpoints.divisions import Division
from mlb.endpoints.venues import Venue, FieldInfo
from mlb.endpoints.sports import Sport


@pytest.fixture(scope="module")
def client():
    return MLBClient()


# --- Leagues ---

def test_leagues_list(client):
    leagues = client.leagues.list()
    assert len(leagues) >= 2
    assert all(isinstance(l, League) for l in leagues)


def test_leagues_al_nl(client):
    leagues = client.leagues.list()
    ids = {l.id for l in leagues}
    assert 103 in ids  # AL
    assert 104 in ids  # NL


def test_league_get(client):
    al = client.leagues.get(103)
    assert al.id == 103
    assert "American" in al.name
    assert al.num_teams == 15


def test_league_season_dates(client):
    al = client.leagues.get(103)
    if al.season_dates:
        assert al.season_dates.season_start is not None


# --- Divisions ---

def test_divisions_list(client):
    divs = client.divisions.list()
    assert len(divs) == 6
    assert all(isinstance(d, Division) for d in divs)


def test_division_get(client):
    from mlb.endpoints.divisions import DivisionsEndpoint
    nl_west = client.divisions.get(DivisionsEndpoint.NL_WEST)
    assert nl_west.id == 203
    assert "NL West" in nl_west.name or "National League West" in nl_west.name


# --- Venues ---

def test_venue_get(client):
    # Dodger Stadium = 22
    venue = client.venues.get(22)
    assert isinstance(venue, Venue)
    assert venue.id == 22
    assert "Dodger" in venue.name
    assert venue.city == "Los Angeles"
    assert venue.state_abbrev == "CA"


def test_venue_field_info(client):
    venue = client.venues.get(22)
    fi = venue.field_info
    assert isinstance(fi, FieldInfo)
    assert fi.capacity and fi.capacity > 40000
    assert fi.center and fi.center > 390


def test_venue_coordinates(client):
    venue = client.venues.get(22)
    assert venue.latitude is not None
    assert venue.longitude is not None
    assert 33 < venue.latitude < 35  # LA is ~34°N
    assert -119 < venue.longitude < -117  # LA is ~-118°W


def test_venue_list_multiple(client):
    venues = client.venues.list(venue_ids=[22, 3313])  # Dodger Stadium, Yankee Stadium
    assert len(venues) == 2


# --- Sports ---

def test_sports_list(client):
    sports = client.sports.list()
    assert len(sports) >= 10
    assert all(isinstance(s, Sport) for s in sports)


def test_sports_mlb(client):
    mlb = client.sports.get(1)
    assert mlb.id == 1
    assert "Major League Baseball" in mlb.name or mlb.abbreviation == "MLB"
