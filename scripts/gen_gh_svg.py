"""Regenerates assets/github.svg from the GitHub API.

Run: python scripts/gen_gh_svg.py
Also run nightly by .github/workflows/dsa-stats.yml.

Replaces github-readme-stats and github-readme-activity-graph, which were
returning 503 and 402 respectively and rendering as broken images. Set
GITHUB_TOKEN to lift the 60/hr anonymous rate limit (the workflow does).
"""
import json
import os
import pathlib
import urllib.error
import urllib.request

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "github.svg"
USER = "Abhishek86798"

GQL = """
query($u: String!) {
  user(login: $u) {
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false,
                 orderBy: {field: STARGAZERS, direction: DESC}) {
      totalCount
      nodes { stargazerCount primaryLanguage { name } }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar { totalContributions }
    }
    pullRequests(states: MERGED) { totalCount }
  }
}
"""


def api(token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": GQL, "variables": {"u": USER}}).encode(),
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "readme-stats/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["data"]["user"]


TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 176" width="900" height="176" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
  <rect width="900" height="176" rx="12" fill="#0d1117"/>
  <rect x="0.5" y="0.5" width="899" height="175" rx="12" fill="none" stroke="#1f2733"/>

  <text x="36" y="42" fill="#8b949e" font-size="13" font-weight="700" letter-spacing="2">GITHUB</text>
  <text x="864" y="42" fill="#6e7681" font-size="12" text-anchor="end">last 12 months &#183; rebuilt nightly</text>
  <line x1="36" y1="58" x2="864" y2="58" stroke="#1f2733"/>

  <text x="36" y="100" fill="#e6edf3" font-size="30" font-weight="700">{contribs}</text>
  <text x="36" y="120" fill="#6e7681" font-size="11">contributions</text>

  <text x="212" y="100" fill="#e6edf3" font-size="30" font-weight="700">{commits}</text>
  <text x="212" y="120" fill="#6e7681" font-size="11">commits</text>

  <text x="388" y="100" fill="#58a6ff" font-size="30" font-weight="700">{merged}</text>
  <text x="388" y="120" fill="#6e7681" font-size="11">merged PRs</text>

  <text x="564" y="100" fill="#e6edf3" font-size="30" font-weight="700">{repos}</text>
  <text x="564" y="120" fill="#6e7681" font-size="11">public repos</text>

  <text x="740" y="100" fill="#e6edf3" font-size="30" font-weight="700">{stars}</text>
  <text x="740" y="120" fill="#6e7681" font-size="11">stars earned</text>

  <line x1="36" y1="138" x2="864" y2="138" stroke="#1f2733"/>
{langs}
</svg>
"""

LANG_COLORS = {
    "Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a",
    "C++": "#f34b7d", "Go": "#00ADD8", "Java": "#b07219", "C": "#555555",
    "HTML": "#e34c26", "CSS": "#563d7c", "Shell": "#89e051",
    "Jupyter Notebook": "#DA5B0B", "Dockerfile": "#384d54",
}


def lang_bar(nodes):
    """One stacked bar of language share, by repo count."""
    counts = {}
    for n in nodes:
        lang = (n.get("primaryLanguage") or {}).get("name")
        if lang:
            counts[lang] = counts.get(lang, 0) + 1
    if not counts:
        return ""

    top = sorted(counts.items(), key=lambda kv: -kv[1])[:6]
    total = sum(c for _, c in top)
    out, x = [], 36.0
    width = 828.0
    for name, count in top:
        w = width * count / total
        out.append(f'  <rect x="{x:.1f}" y="150" width="{max(w - 2, 2):.1f}" height="6" rx="3" '
                   f'fill="{LANG_COLORS.get(name, "#6e7681")}"/>')
        x += w
    legend = "  ".join(f"{n} {c}" for n, c in top)
    out.append(f'  <text x="36" y="172" fill="#6e7681" font-size="10">{legend}</text>')
    return "\n".join(out)


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set; keeping existing github.svg")
        return 1
    try:
        u = api(token)
    except (urllib.error.URLError, KeyError, TypeError) as e:
        print(f"github fetch failed ({e}); keeping existing github.svg")
        return 1

    repos = u["repositories"]
    cc = u["contributionsCollection"]
    OUT.write_text(TEMPLATE.format(
        contribs=cc["contributionCalendar"]["totalContributions"],
        commits=cc["totalCommitContributions"],
        merged=u["pullRequests"]["totalCount"],
        repos=repos["totalCount"],
        stars=sum(n["stargazerCount"] for n in repos["nodes"]),
        langs=lang_bar(repos["nodes"]),
    ), encoding="utf-8")
    print(f"github.svg: {cc['contributionCalendar']['totalContributions']} contributions, "
          f"{u['pullRequests']['totalCount']} merged PRs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
