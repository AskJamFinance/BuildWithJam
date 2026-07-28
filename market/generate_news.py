#!/usr/bin/env python3
"""Build market/index.html from market/news.json using only Python's standard library."""

from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "news.json"
OUTPUT_PATH = ROOT / "index.html"


def text(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def verified_http_url(value: object) -> str:
    candidate = str(value or "").strip()
    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Invalid article URL: {candidate!r}")
    return html.escape(candidate, quote=True)


def require_story(story: dict, section: str, index: int) -> None:
    required = {"headline", "url", "summary", "source", "published"}
    if section in {"financial", "global"}:
        required.add("why_it_matters")
    missing = sorted(key for key in required if not str(story.get(key, "")).strip())
    if missing:
        raise ValueError(
            f"{section} story {index + 1} is missing: {', '.join(missing)}"
        )
    verified_http_url(story["url"])


def story_card(story: dict, show_why: bool) -> str:
    why = ""
    if show_why:
        why = f"""
          <div class="why">
            <strong>★ WHY IT MATTERS</strong>
            <p>{text(story["why_it_matters"])}</p>
          </div>"""
    return f"""
        <article class="card">
          <h3>
            <a href="{verified_http_url(story["url"])}" target="_blank" rel="noopener noreferrer">
              {text(story["headline"])} <span aria-hidden="true">↗</span>
            </a>
          </h3>
          <p>{text(story["summary"])}</p>
          {why}
          <p class="source">{text(story["source"])} · {text(story["published"])}</p>
        </article>"""


def section(section_id: str, icon: str, title: str, stories: list[dict], show_why: bool) -> str:
    cards = "\n".join(story_card(story, show_why) for story in stories)
    if not cards:
        cards = '<p class="empty">No qualifying stories were selected for this edition.</p>'
    return f"""
      <section class="news-section" id="{section_id}">
        <h2>{icon} {title}</h2>
        {cards}
      </section>"""


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for section_name in ("singapore", "financial", "global"):
        stories = data.get(section_name, [])
        if not isinstance(stories, list):
            raise ValueError(f"{section_name} must be a list")
        for index, story in enumerate(stories):
            require_story(story, section_name, index)

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="BuildWithJam Daily Market News Brief">
  <title>BuildWithJam Daily Market News Brief</title>
  <style>
    :root {{
      --navy: #0B2F68;
      --gold: #F3BA3B;
      --green: #23843B;
      --purple: #7244AA;
      --ink: #152033;
      --muted: #64748b;
      --line: #dbe3ee;
      --paper: #FFFFFF;
      --soft: #f4f7fb;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      background: var(--soft);
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.55;
    }}
    a {{ color: inherit; }}
    .shell {{ width: min(1180px, calc(100% - 32px)); margin: 28px auto; }}
    .hero {{
      display: grid;
      grid-template-columns: 1.35fr .65fr;
      gap: 34px;
      align-items: center;
      overflow: hidden;
      padding: clamp(28px, 5vw, 64px);
      color: white;
      background: linear-gradient(135deg, #071f49, var(--navy) 62%, #174c98);
      border-radius: 24px 24px 0 0;
    }}
    .eyebrow {{
      margin: 0 0 12px;
      color: var(--gold);
      font-weight: 800;
      letter-spacing: .12em;
      text-transform: uppercase;
    }}
    h1 {{ max-width: 720px; margin: 0; font-size: clamp(2.4rem, 6vw, 5.1rem); line-height: .95; }}
    .subtitle {{ max-width: 650px; margin: 22px 0 14px; font-size: 1.08rem; color: #e8eef8; }}
    .date {{ margin: 0; font-weight: 700; }}
    .hero img {{
      width: 100%;
      max-height: 340px;
      object-fit: contain;
      filter: drop-shadow(0 18px 24px rgba(0,0,0,.25));
    }}
    nav {{
      position: sticky;
      top: 0;
      z-index: 5;
      display: flex;
      gap: 9px;
      padding: 13px clamp(16px, 3vw, 30px);
      overflow-x: auto;
      background: white;
      border-bottom: 1px solid var(--line);
      box-shadow: 0 8px 20px rgba(11,47,104,.08);
    }}
    nav a {{
      flex: 0 0 auto;
      padding: 9px 13px;
      color: var(--navy);
      font-size: .9rem;
      font-weight: 700;
      text-decoration: none;
      border-radius: 999px;
      background: #edf3fb;
    }}
    .columns {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 20px;
      padding: 28px;
      background: white;
    }}
    .news-section {{ min-width: 0; scroll-margin-top: 80px; }}
    h2 {{ min-height: 62px; margin: 0 0 14px; color: var(--navy); font-size: 1.1rem; line-height: 1.25; }}
    .card {{
      margin-bottom: 16px;
      padding: 20px;
      border: 1px solid var(--line);
      border-radius: 16px;
      background: white;
      box-shadow: 0 8px 22px rgba(11,47,104,.07);
    }}
    .card h3 {{ margin: 0 0 11px; color: var(--navy); font-size: 1.04rem; line-height: 1.35; }}
    .card h3 a {{ text-decoration-thickness: 1px; text-underline-offset: 3px; }}
    .card h3 a:hover {{ color: var(--purple); }}
    .card p {{ margin: 0 0 13px; }}
    .why {{ padding: 13px; border-left: 4px solid var(--gold); border-radius: 9px; background: #fff8e5; }}
    .why strong {{ color: var(--navy); font-size: .77rem; letter-spacing: .06em; }}
    .why p {{ margin: 6px 0 0; font-size: .9rem; }}
    .source {{ margin-bottom: 0 !important; color: var(--muted); font-size: .78rem; font-weight: 700; }}
    .empty {{ color: var(--muted); font-style: italic; }}
    .thought {{
      scroll-margin-top: 80px;
      padding: 34px clamp(24px, 5vw, 58px);
      color: white;
      text-align: center;
      background: var(--purple);
    }}
    .thought h2 {{ min-height: auto; color: white; }}
    .thought p {{ max-width: 780px; margin: auto; font-size: clamp(1.15rem, 2.5vw, 1.55rem); }}
    .cta {{ padding: 38px 24px; text-align: center; background: white; }}
    .cta p {{ margin-top: 0; font-weight: 700; }}
    .button {{
      display: inline-block;
      padding: 13px 21px;
      color: white;
      font-weight: 800;
      text-decoration: none;
      border-radius: 10px;
      background: var(--green);
    }}
    footer {{ padding: 28px; color: #dbe6f5; text-align: center; background: #071f49; border-radius: 0 0 24px 24px; }}
    footer strong {{ color: var(--gold); }}
    footer p {{ max-width: 820px; margin: 7px auto; font-size: .82rem; }}
    @media (max-width: 840px) {{
      .shell {{ width: 100%; margin: 0; }}
      .hero {{ grid-template-columns: 1fr; border-radius: 0; }}
      .hero-media {{ order: -1; }}
      .hero img {{ max-height: 210px; }}
      .columns {{ grid-template-columns: 1fr; padding: 22px 16px; }}
      h2 {{ min-height: auto; margin-top: 12px; }}
      footer {{ border-radius: 0; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <header class="hero">
      <div>
        <p class="eyebrow">☀ {text(data.get("edition", "MARKET BRIEF"))}</p>
        <h1>DAILY MARKET<br>NEWS BRIEF</h1>
        <p class="subtitle">{text(data.get("subtitle", ""))}</p>
        <p class="date">{text(data.get("date", ""))} · LAST 24 HOURS</p>
      </div>
      <div class="hero-media">
        <img src="assets/jamica-market-news.png" alt="Jamica reading the morning financial news">
      </div>
    </header>

    <nav aria-label="Newsletter sections">
      <a href="#singapore">🇸🇬 Singapore Headlines</a>
      <a href="#financial">📈 Financial Updates</a>
      <a href="#global">🌍 Global Markets</a>
      <a href="#thought">💡 Thought of the Day</a>
    </nav>

    <div class="columns">
      {section("singapore", "🇸🇬", "SINGAPORE HEADLINES", data["singapore"], False)}
      {section("financial", "📈", "SINGAPORE FINANCIAL UPDATES", data["financial"], True)}
      {section("global", "🌍", "GLOBAL MARKET UPDATES", data["global"], True)}
    </div>

    <section class="thought" id="thought">
      <h2>💡 THOUGHT OF THE DAY</h2>
      <p>{text(data.get("thought", ""))}</p>
    </section>

    <section class="cta">
      <p>Have a question about what today's markets could mean for your financial plan?</p>
      <a class="button" href="https://wa.me/6590694815" target="_blank" rel="noopener noreferrer">💬 WhatsApp Jamica</a>
    </section>

    <footer>
      <strong>#BuildWithJam</strong>
      <p>Daily Market News Brief</p>
      <p>General information only. This newsletter does not constitute financial advice or a recommendation to buy or sell any investment or insurance product.</p>
    </footer>
  </main>
</body>
</html>
"""
    OUTPUT_PATH.write_text(document, encoding="utf-8")
    print(f"Generated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
