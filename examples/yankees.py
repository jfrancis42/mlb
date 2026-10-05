#!/usr/bin/env python3
"""Yankees dashboard — roster, standings, schedule, and recent results."""

from mlb import MLBClient
from mlb.endpoints.teams import TeamsEndpoint

YANKEES = TeamsEndpoint.YANKEES


def rule(char="─", width=60):
    print(char * width)


def section(title):
    rule()
    print(f"  {title}")
    rule()


def main():
    client = MLBClient()

    # ── Team info ─────────────────────────────────────────────────────────────
    team = client.teams.get(YANKEES)
    venue = client.venues.get(team.venue_id)

    section("NEW YORK YANKEES")
    print(f"  Full name:    {team.name}")
    print(f"  Division:     {team.division_name}")
    print(f"  League:       {team.league_name}")
    print(f"  Founded:      {team.first_year_of_play}")
    print(f"  Ballpark:     {venue.name}, {venue.city}, {venue.state_abbrev}")
    if venue.field_info:
        fi = venue.field_info
        print(f"  Capacity:     {fi.capacity:,}")
        print(f"  Dimensions:   LF {fi.left_line}  LC {fi.left_center}  CF {fi.center}  RC {fi.right_center}  RF {fi.right_line}")
        print(f"  Surface:      {fi.turf_type}  /  {fi.roof_type} roof")

    # ── Division standings ────────────────────────────────────────────────────
    section("AL EAST STANDINGS")
    all_standings = client.standings.get(league_ids=[103])
    al_east = next((d for d in all_standings if d.division_id == 201), None)

    if al_east:
        header = f"  {'#':<3} {'Team':<28} {'W':>4} {'L':>4} {'PCT':>6} {'GB':>6} {'STRK':>6}"
        print(header)
        print("  " + "·" * 58)
        for tr in al_east.team_records:
            marker = "◀" if tr.team_id == YANKEES else " "
            streak = tr.streak.code if tr.streak else "—"
            gb = "  —   " if tr.games_back == "-" else f"{tr.games_back:>6}"
            print(f"  {tr.division_rank:<3} {tr.team_name:<28} {tr.wins:>4} {tr.losses:>4} "
                  f"{tr.winning_pct:>6} {gb} {streak:>5}  {marker}")

    # ── Active roster ─────────────────────────────────────────────────────────
    section("ACTIVE ROSTER")
    roster = client.teams.roster(YANKEES, roster_type="active")

    # Group by position type
    by_type: dict[str, list] = {}
    for player in sorted(roster, key=lambda r: (r.position_type, r.jersey_number or "99")):
        by_type.setdefault(player.position_type, []).append(player)

    for pos_type in ["Pitcher", "Catcher", "Infielder", "Outfielder", "Hitter", "Two-Way Player"]:
        players = by_type.get(pos_type, [])
        if not players:
            continue
        print(f"\n  {pos_type}s")
        for p in players:
            num = f"#{p.jersey_number}" if p.jersey_number else "   "
            print(f"    {num:<5}  {p.person_name:<28}  {p.position_abbreviation}")

    # ── Schedule: last 5 results + next 5 games ───────────────────────────────
    section("RECENT RESULTS & UPCOMING")
    full_sched = client.schedule.for_team(YANKEES, season=2026)

    final_games = [g for g in full_sched.games if g.status.is_final]
    upcoming = [g for g in full_sched.games if g.status.is_preview]

    print("\n  Last 5 results:")
    for game in final_games[-5:]:
        if game.home.team_id == YANKEES:
            opp = game.away.team_name
            location = "vs"
            yank_score = game.home.score
            opp_score = game.away.score
        else:
            opp = game.home.team_name
            location = "@"
            yank_score = game.away.score
            opp_score = game.home.score

        result = "W" if (yank_score is not None and opp_score is not None and yank_score > opp_score) else "L"
        score_str = f"{yank_score}-{opp_score}" if yank_score is not None else "—"
        print(f"    {game.official_date}  {result}  {location} {opp:<25}  {score_str}")

    print("\n  Next 5 games:")
    for game in upcoming[:5]:
        if game.home.team_id == YANKEES:
            opp = game.away.team_name
            location = "vs"
        else:
            opp = game.home.team_name
            location = "@"
        time_str = game.game_date[11:16] if len(game.game_date) > 16 else ""
        print(f"    {game.official_date}  {game.day_night.upper():<5}  {location} {opp:<25}  {time_str} UTC")

    # ── Key hitters: current season stats ─────────────────────────────────────
    section("LINEUP — 2026 HITTING STATS")

    position_players = [
        p for p in roster
        if p.position_type in ("Catcher", "Infielder", "Outfielder", "Hitter", "Two-Way Player")
    ]

    print(f"  {'Player':<28} {'#':>3}  {'AVG':>5} {'HR':>4} {'RBI':>5} {'OPS':>6} {'SB':>4}")
    print("  " + "·" * 58)

    for entry in sorted(position_players, key=lambda r: r.jersey_number or "99"):
        stat_groups = client.players.stats(
            entry.person_id,
            groups=["hitting"],
            stat_type="season",
            season=2026,
        )
        stat = {}
        for group in stat_groups:
            for split in group.splits:
                if split.game_type == "R":
                    stat = split.stat
                    break

        avg = stat.get("avg", ".---")
        home_runs = stat.get("homeRuns", "-")
        rbi = stat.get("rbi", "-")
        ops = stat.get("ops", ".---")
        sb = stat.get("stolenBases", "-")
        num = f"#{entry.jersey_number}" if entry.jersey_number else "   "
        print(f"  {entry.person_name:<28} {num:>4}  {avg:>5} {home_runs:>4} {rbi:>5} {ops:>6} {sb:>4}")

    rule()
    print()


if __name__ == "__main__":
    main()
