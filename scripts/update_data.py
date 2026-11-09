#!/usr/bin/env python3
"""Fetch daily sports data from API-SPORTS and write data/sports.json."""
import json, os, sys, urllib.parse, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "sports.json"
KEY = os.environ.get("APISPORTS_KEY", "").strip()
if not KEY:
    raise SystemExit("Missing APISPORTS_KEY repository secret.")

# The workflow runs at 05:00 and 06:00 UTC. Only the Paris 07:00 run proceeds,
# which automatically handles CET/CEST without a fixed-UTC daylight-saving bug.
now = datetime.now(ZoneInfo("Europe/Paris"))
if os.environ.get("FORCE_REFRESH") != "1" and not (now.hour == 7):
    print(f"Skip: Paris time is {now:%H:%M}; scheduled refresh is 07:00.")
    raise SystemExit(0)

def api(base, endpoint, params):
    url = base + endpoint + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"x-apisports-key": KEY, "User-Agent": "SPORT-LIVE/1.0"})
    with urllib.request.urlopen(req, timeout=40) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if payload.get("errors"):
        raise RuntimeError(f"{endpoint}: {payload['errors']}")
    return payload.get("response", [])

football_base = "https://v3.football.api-sports.io/"
basket_base = "https://v1.basketball.api-sports.io/"
season = now.year if now.month >= 7 else now.year - 1
football_leagues = {
    "laliga": {"id": 140, "name": "La Liga"},
    "ligue1": {"id": 61, "name": "Ligue 1"},
    "epl": {"id": 39, "name": "Premier League"},
}
newdata = {"generated_at": now.isoformat(), "timezone": "Europe/Paris", "football": {}, "nba": {}}

# 6 calls total for football: one standings + one season fixture feed per competition.
for key, league in football_leagues.items():
    params = {"league": league["id"], "season": season}
    standings = api(football_base, "standings", params)
    fixtures = api(football_base, "fixtures", {**params, "timezone": "Europe/Paris"})
    newdata["football"][key] = {
        "name": league["name"], "league_id": league["id"], "season": season,
        "standings": standings, "fixtures": fixtures
    }
    print(f"{league['name']}: {len(fixtures)} fixtures")

# API-Basketball: NBA league id 12. One call for standings, one for the season schedule/results.
nba_season = f"{season}-{season+1}"
nba_params = {"league": 12, "season": nba_season}
nba_standings = api(basket_base, "standings", nba_params)
nba_games = api(basket_base, "games", {**nba_params, "timezone": "Europe/Paris"})
newdata["nba"] = {"league_id": 12, "season": nba_season, "standings": nba_standings, "games": nba_games}
print(f"NBA: {len(nba_games)} games")

OUT.parent.mkdir(parents=True, exist_ok=True)
tmp = OUT.with_suffix(".tmp")
tmp.write_text(json.dumps(newdata, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
tmp.replace(OUT)
print(f"Updated {OUT} at {now:%Y-%m-%d %H:%M %Z}")
