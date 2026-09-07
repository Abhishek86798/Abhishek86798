"""Regenerates assets/dsa.svg from live platform APIs.

Run: python scripts/gen_dsa_svg.py
Also run nightly by .github/workflows/dsa-stats.yml, which commits the
result if it changed.

Codolio has no public stats API — every route on api.codolio.com needs a
bearer token, and /card/grid.svg is only a decorative background. So the
totals are rebuilt here from the platforms Codolio itself aggregates.
LeetCode's GraphQL is public; GFG and Code360 are not, so those counts
live in FALLBACK below and are bumped by hand.
"""
import json
import pathlib
import urllib.error
import urllib.request

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "dsa.svg"

LEETCODE_USER = "abhiii1005_"

# Platforms without a public API. Update when the numbers move.
# ponytail: hand-maintained, wire up a real fetch if either exposes one.
# Reconciled against the Codolio profile so the total matches what that
# page shows. LeetCode is fetched live; these three are not.
FALLBACK = {
    "gfg": 285,        # geeksforgeeks, incl. 25 GFG Basic
    "code360": 155,    # naukri code360, 4x monthly topper
    "codechef": 107,   # codechef
}
# Contests on platforms without a public API (codechef 9 + code360 6).
FALLBACK_CONTESTS = 15

QUERY = """
query($u: String!) {
  matchedUser(username: $u) {
    submitStatsGlobal { acSubmissionNum { difficulty count } }
  }
  userContestRanking(username: $u) {
    rating
    attendedContestsCount
    topPercentage
  }
}
"""


def fetch_leetcode(user):
    """Public GraphQL. Returns (by_difficulty, rating, contests)."""
    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"u": user}}).encode(),
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            # LeetCode 403s the default urllib agent.
            "User-Agent": "Mozilla/5.0 (compatible; readme-stats/1.0)",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)["data"]

    counts = {
        d["difficulty"].lower(): d["count"]
        for d in data["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]
    }
    ranking = data.get("userContestRanking") or {}
    return (counts, round(ranking.get("rating", 0)),
            ranking.get("attendedContestsCount", 0),
            round(ranking.get("topPercentage", 0), 1))


TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 150" width="900" height="150" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
  <rect width="900" height="150" rx="12" fill="#0d1117"/>
  <rect x="0.5" y="0.5" width="899" height="149" rx="12" fill="none" stroke="#1f2733"/>

  <text x="36" y="42" fill="#8b949e" font-size="13" font-weight="700" letter-spacing="2">DSA</text>
  <text x="864" y="42" fill="#6e7681" font-size="12" text-anchor="end">live &#183; rebuilt nightly</text>
  <line x1="36" y1="58" x2="864" y2="58" stroke="#1f2733"/>

  <text x="36" y="102" fill="#e6edf3" font-size="34" font-weight="700">{total}</text>
  <text x="36" y="124" fill="#6e7681" font-size="12">solved</text>

  <line x1="212" y1="76" x2="212" y2="126" stroke="#1f2733"/>

  <text x="248" y="102" fill="#58a6ff" font-size="34" font-weight="700">{rating}</text>
  <text x="248" y="124" fill="#6e7681" font-size="12">leetcode rating &#183; top {toppct}%</text>

  <line x1="470" y1="76" x2="470" y2="126" stroke="#1f2733"/>

  <text x="506" y="102" fill="#e6edf3" font-size="34" font-weight="700">{contests}</text>
  <text x="506" y="124" fill="#6e7681" font-size="12">contests</text>

  <line x1="638" y1="76" x2="638" y2="126" stroke="#1f2733"/>

  <text x="674" y="88" fill="#6e7681" font-size="10" letter-spacing="1">LEETCODE SPLIT</text>
  <text x="674" y="112" fill="#3fb950" font-size="14" font-weight="700">{easy}</text>
  <text x="674" y="128" fill="#6e7681" font-size="10">easy</text>
  <text x="748" y="112" fill="#d29922" font-size="14" font-weight="700">{medium}</text>
  <text x="748" y="128" fill="#6e7681" font-size="10">medium</text>
  <text x="838" y="112" fill="#f85149" font-size="14" font-weight="700">{hard}</text>
  <text x="838" y="128" fill="#6e7681" font-size="10">hard</text>
</svg>
"""


def main():
    try:
        lc, rating, contests, toppct = fetch_leetcode(LEETCODE_USER)
    except (urllib.error.URLError, KeyError, TypeError) as e:
        # Leave the committed SVG alone rather than publishing zeroes.
        print(f"leetcode fetch failed ({e}); keeping existing {OUT.name}")
        return 1

    total = lc["all"] + sum(FALLBACK.values())
    OUT.write_text(TEMPLATE.format(
        total=total, rating=rating, contests=contests + FALLBACK_CONTESTS,
        toppct=toppct,
        easy=lc["easy"], medium=lc["medium"], hard=lc["hard"],
    ), encoding="utf-8")
    print(f"{OUT.name}: {total} solved, rating {rating}, {contests + FALLBACK_CONTESTS} contests, "
          f"{lc['easy']}/{lc['medium']}/{lc['hard']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
