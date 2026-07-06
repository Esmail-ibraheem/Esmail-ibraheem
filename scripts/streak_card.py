#!/usr/bin/env python3
"""Generate assets/streak.svg — terminal-style contribution streak card.

Run daily by .github/workflows/streak.yml with the default GITHUB_TOKEN.
Queries the GraphQL contribution calendar year by year, computes total
contributions plus current/longest streaks, and renders the card in the
same palette, grid, and 20s animation loop as hero.svg / stats-v2.svg.
Stdlib only — no dependencies to install in CI.
"""
import datetime as dt
import json
import os
import sys
import urllib.request

LOGIN = "Esmail-ibraheem"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "streak.svg")
API = "https://api.github.com/graphql"

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def gql(query, variables, token):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        API, data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data["data"]


def fetch_calendar(token):
    """Return (days: {iso-date: count}, total: int, created: iso-date)."""
    created = gql("query($login: String!) { user(login: $login) { createdAt } }",
                  {"login": LOGIN}, token)["user"]["createdAt"][:10]
    first_year = int(created[:4])
    now = dt.datetime.now(dt.timezone.utc)
    days, total = {}, 0
    for year in range(first_year, now.year + 1):
        # Clamp the current year's window to now: a window reaching into the
        # future makes the calendar return future days as zero-count entries.
        to = f"{year}-12-31T23:59:59Z" if year < now.year else f"{now:%Y-%m-%dT%H:%M:%S}Z"
        cal = gql(QUERY, {"login": LOGIN,
                          "from": f"{year}-01-01T00:00:00Z",
                          "to": to},
                  token)["user"]["contributionsCollection"]["contributionCalendar"]
        total += cal["totalContributions"]
        for week in cal["weeks"]:
            for day in week["contributionDays"]:
                days[day["date"]] = day["contributionCount"]
    return days, total, created


def compute_streaks(days, today):
    """Current and longest runs of consecutive days with contributions.

    A zero-count `today` does not break the current streak — it can still
    be extended before midnight. Missing dates count as gaps.
    """
    active = {d for d, c in days.items() if c > 0 and d <= today}
    if not active:
        return {"current": 0, "longest": 0, "current_range": None, "longest_range": None}

    one = dt.timedelta(days=1)

    def to_date(s):
        return dt.date.fromisoformat(s)

    longest, longest_range = 0, None
    run_start = None
    prev = None
    for d in sorted(to_date(s) for s in active):
        if prev is None or d - prev > one:
            run_start = d
        if (d - run_start).days + 1 > longest:
            longest = (d - run_start).days + 1
            longest_range = (run_start.isoformat(), d.isoformat())
        prev = d

    cursor = to_date(today)
    if cursor.isoformat() not in active:
        cursor -= one  # today may still get contributions
    current, current_range = 0, None
    end = cursor
    while cursor.isoformat() in active:
        current += 1
        current_range = (cursor.isoformat(), end.isoformat())
        cursor -= one
    return {"current": current, "longest": longest,
            "current_range": current_range, "longest_range": longest_range}


def derive_today(days, now_iso):
    """Last calendar day, but never a future date the API might return."""
    return min(max(days), now_iso) if days else now_iso


def fmt_days(n):
    return f"{n} day" + ("" if n == 1 else "s")


def fmt_range(r):
    return f"{r[0]} → {r[1]}" if r else "—"


def render_svg(total, since, streaks, updated):
    cur, lon = streaks["current"], streaks["longest"]
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 170" width="840" height="170" role="img" aria-label="Contribution streak, updated {updated}: {total:,} total contributions since {since}; current streak {fmt_days(cur)}; longest streak {fmt_days(lon)}.">
  <style>
    text {{
      font-family: ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, 'DejaVu Sans Mono', monospace;
      font-size: 14px;
      fill: #F0EEE6;
    }}
    .t12 {{ font-size: 12px; }}
    .dim {{ fill: #8A8A82; }}
    .coral {{ fill: #D97757; }}
    .n {{ font-size: 26px; font-weight: 700; }}

    /* Same grammar as hero.svg/stats-v2.svg: chrome persists, content
       loops on a 20s timeline; base styles equal the final frame. */
    #panel {{ animation: winIn 0.4s ease-out 1; }}
    #scene {{ animation: scene 20s linear infinite; }}
    #hdr {{ animation: hdr 20s linear infinite; }}
    #c1 {{ animation: c1 20s linear infinite; }}
    #c2 {{ animation: c2 20s linear infinite; }}
    #c3 {{ animation: c3 20s linear infinite; }}

    @keyframes winIn {{ 0% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
    @keyframes scene {{ 0%, 92.5% {{ opacity: 1; }} 97%, 100% {{ opacity: 0; }} }}
    @keyframes hdr {{ 0%, 2% {{ opacity: 0; }} 4%, 100% {{ opacity: 1; }} }}
    @keyframes c1 {{ 0%, 5% {{ opacity: 0; transform: translateY(5px); }} 7%, 100% {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes c2 {{ 0%, 8% {{ opacity: 0; transform: translateY(5px); }} 10%, 100% {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes c3 {{ 0%, 11% {{ opacity: 0; transform: translateY(5px); }} 13%, 100% {{ opacity: 1; transform: translateY(0); }} }}

    @media (prefers-reduced-motion: reduce) {{
      #panel, #scene, #hdr, #c1, #c2, #c3 {{ animation: none; }}
    }}
  </style>

  <g id="panel">
    <rect x="0.5" y="0.5" width="839" height="169" rx="12" fill="#1F1E1D" stroke="#3E3E38"/>
  </g>

  <g id="scene">
    <g id="hdr">
      <text class="t12 dim" x="32" y="42"># streak · updated {updated} · refreshed daily</text>
      <line x1="300.5" y1="58" x2="300.5" y2="146" stroke="#3E3E38"/>
      <line x1="540.5" y1="58" x2="540.5" y2="146" stroke="#3E3E38"/>
    </g>

    <g id="c1">
      <text class="n" x="166" y="100" text-anchor="middle">{total:,}</text>
      <text class="t12 dim" x="166" y="124" text-anchor="middle">total contributions</text>
      <text class="t12 dim" x="166" y="144" text-anchor="middle">since {since}</text>
    </g>

    <g id="c2">
      <text class="n coral" x="420" y="100" text-anchor="middle">✻ {fmt_days(cur)}</text>
      <text class="t12 dim" x="420" y="124" text-anchor="middle">current streak</text>
      <text class="t12 dim" x="420" y="144" text-anchor="middle">{fmt_range(streaks["current_range"])}</text>
    </g>

    <g id="c3">
      <text class="n" x="674" y="100" text-anchor="middle">{fmt_days(lon)}</text>
      <text class="t12 dim" x="674" y="124" text-anchor="middle">longest streak</text>
      <text class="t12 dim" x="674" y="144" text-anchor="middle">{fmt_range(streaks["longest_range"])}</text>
    </g>
  </g>
</svg>
"""


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    token = os.environ["GITHUB_TOKEN"]
    days, total, created = fetch_calendar(token)
    today = derive_today(days, dt.datetime.now(dt.timezone.utc).date().isoformat())
    streaks = compute_streaks(days, today)
    svg = render_svg(total, created, streaks, today)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"total={total:,} since={created} current={streaks['current']} "
          f"{fmt_range(streaks['current_range'])} longest={streaks['longest']} "
          f"{fmt_range(streaks['longest_range'])} -> {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
