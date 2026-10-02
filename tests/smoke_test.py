import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE_URL = os.getenv("PLUTON_BASE_URL", "http://localhost:8000")


def request_json(method, path, payload=None, token=None):
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body else None
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"error": body}
        raise RuntimeError(f"HTTP {exc.code} on {method} {path}: {payload}") from exc
    except Exception as exc:  # pragma: no cover - smoke test only
        raise RuntimeError(f"Request failed for {method} {path}: {exc}") from exc


def require_ok(label, result):
    status, payload = result
    if status not in (200, 201):
        raise RuntimeError(f"{label} failed with status {status}: {payload}")
    return payload


def wait_for_server(timeout_seconds=20):
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            status, payload = request_json("GET", "/health")
            if status == 200:
                return
        except Exception:
            time.sleep(1)
    raise RuntimeError("Server did not start in time at %s" % BASE_URL)


def smoke_test():
    print(f"Waiting for server at {BASE_URL}...")
    wait_for_server()

    print("Checking /health and /ready...")
    require_ok("health", request_json("GET", "/health"))
    require_ok("ready", request_json("GET", "/ready"))

    print("Creating sport...")
    sport = require_ok(
        "create sport",
        request_json(
            "POST",
            "/api/v1/sports",
            {
                "code": "SMOKE_FOOTBALL",
                "name": "Smoke Football",
                "active": True,
            },
        ),
    )

    print("Creating league...")
    league = require_ok(
        "create league",
        request_json(
            "POST",
            "/api/v1/leagues",
            {
                "sport_id": sport["id"],
                "code": "SMOKE_LEAGUE",
                "name": "Smoke League",
                "country": "Testland",
                "is_international": False,
                "active": True,
            },
        ),
    )

    print("Creating season...")
    season = require_ok(
        "create season",
        request_json(
            "POST",
            "/api/v1/seasons",
            {
                "league_id": league["id"],
                "name": "2024/25",
                "start_date": "2024-08-01",
                "end_date": "2025-05-31",
                "active": True,
                "is_archived": False,
                "is_locked": False,
                "version": 1,
                "protected_from_auto_update": True,
            },
        ),
    )

    print("Creating home team...")
    home_team = require_ok(
        "create home team",
        request_json(
            "POST",
            "/api/v1/teams",
            {
                "sport_id": sport["id"],
                "external_id": "smoke-home-001",
                "name": "Smoke Home FC",
                "short_name": "SHF",
                "country": "Testland",
                "logo_url": "https://example.com/home.png",
                "active": True,
            },
        ),
    )

    print("Creating away team...")
    away_team = require_ok(
        "create away team",
        request_json(
            "POST",
            "/api/v1/teams",
            {
                "sport_id": sport["id"],
                "external_id": "smoke-away-001",
                "name": "Smoke Away FC",
                "short_name": "SAF",
                "country": "Testland",
                "logo_url": "https://example.com/away.png",
                "active": True,
            },
        ),
    )

    print("Creating fixture...")
    fixture = require_ok(
        "create fixture",
        request_json(
            "POST",
            "/api/v1/fixtures",
            {
                "sport_id": sport["id"],
                "league_id": league["id"],
                "season_id": season["id"],
                "external_id": "smoke-fixture-001",
                "event_id": "smoke-event-001",
                "home_team_id": home_team["id"],
                "away_team_id": away_team["id"],
                "kickoff_at": "2025-02-15T18:00:00Z",
                "status": "scheduled",
                "venue": "Smoke Stadium",
                "round_name": "Round 1",
                "competition_name": "Smoke League",
            },
        ),
    )

    print("Registering user...")
    user = require_ok(
        "register user",
        request_json(
            "POST",
            "/auth/register",
            {
                "email": "smoke-user@example.com",
                "username": "smokeuser",
                "password": "password123",
                "full_name": "Smoke User",
            },
        ),
    )
    token = user["access_token"]

    print("Creating prediction...")
    prediction = require_ok(
        "create prediction",
        request_json(
            "POST",
            "/api/v1/predictions",
            {
                "fixture_id": fixture["id"],
                "prediction_type": "match_result",
                "home_score": 2,
                "away_score": 1,
                "market_type": "1x2",
                "confidence": 78.5,
                "strength": 82.0,
            },
            token=token,
        ),
    )

    print("Fetching predictions...")
    predictions = require_ok(
        "get predictions",
        request_json("GET", "/api/v1/predictions", token=token),
    )

    if not isinstance(predictions, list):
        raise RuntimeError(f"Expected list from /api/v1/predictions but got: {predictions!r}")

    print("SMOKE TEST PASSED")
    print(json.dumps({
        "sport": sport,
        "league": league,
        "season": season,
        "home_team": home_team,
        "away_team": away_team,
        "fixture": fixture,
        "user": {"id": user["user"]["id"], "email": user["user"]["email"]},
        "prediction": prediction,
        "prediction_count": len(predictions),
    }, indent=2))


if __name__ == "__main__":
    try:
        smoke_test()
    except Exception as exc:
        print(f"SMOKE TEST FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
