import os
import html
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import feedparser


# --------------------------------------
# 1. Singapore time
# --------------------------------------

SGT = ZoneInfo("Asia/Singapore")

now_sg = datetime.now(SGT)

today_text = now_sg.strftime(
    "%d %B %Y"
)


# --------------------------------------
# 2. RSS FEEDS
# --------------------------------------
#
# Add RSS feeds here.
#
# Start with a small list.
# Replace/add official feed URLs
# that you want to use.
# --------------------------------------

FEEDS = {

    "Singapore Headlines": [
        {
            "name": "CNA",
            "url": "https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml"
        }
    ],

    "Financial Updates": [
        {
            "name": "MAS",
            "url": "https://www.mas.gov.sg/rss/newsroom"
        }
    ],

    "Global Markets": [
        {
            "name": "Reuters",
            "url": "https://feeds.reuters.com/reuters/businessNews"
        }
    ]
}


# --------------------------------------
# 3. Convert RSS dates
# --------------------------------------

def get_entry_date(entry):

    if hasattr(entry, "published_parsed") and entry.published_parsed:

        return datetime(
            *entry.published_parsed[:6],
            tzinfo=timezone.utc
        )

    if hasattr(entry, "updated_parsed") and entry.updated_parsed:

        return datetime(
            *entry.updated_parsed[:6],
            tzinfo=timezone.utc
        )

    return None


# --------------------------------------
# 4. Get stories from last 24 hours
# --------------------------------------

def fetch_recent_stories(feed_list, maximum=5):

    stories = []

    cutoff = datetime.now(
        timezone.utc
    ) - timedelta(hours=24)

    for feed_info in feed_list:

        feed = feedparser.parse(
            feed_info["url"]
        )

        for entry in feed.entries:

            published = get_entry_date(entry)

            if published is None:
                continue

            if published < cutoff:
                continue

            title = getattr(
                entry,
                "title",
                "Untitled"
            )

            link = getattr(
                entry,
                "link",
                "#"
            )

            summary = getattr(
                entry,
                "summary",
                ""
            )

            stories.append(
                {
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "source": feed_info["name"],
                    "published": published
                }
            )


    stories.sort(
        key=lambda story: story["published"],
        reverse=True
    )

    return stories[:maximum]


# --------------------------------------
# 5. Remove ugly HTML from RSS summary
# --------------------------------------

def clean_summary(text):

    text = html.unescape(text)

    # Keep preview short
    if len(text) > 280:

        text = text[:277] + "..."

    return text


# --------------------------------------
# 6. Create one news card
# --------------------------------------

def make_story_html(story, number):

    title = html.escape(
        story["title"]
    )

    link = html.escape(
        story["link"],
        quote=True
    )

    source = html.escape(
        story["source"]
    )

    summary = clean_summary(
        story["summary"]
    )

    date = story["published"].astimezone(
        SGT
    ).strftime(
        "%d %b %Y, %I:%M %p"
    )

    return f"""
    <article class="story">

        <div class="number">
            {number}
        </div>

        <div>

            <h3>

                <a
                    href="{link}"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    {title} ↗
                </a>

            </h3>

            <div class="summary">
                {summary}
            </div>

            <div class="source">
                {source} · {date}
            </div>

        </div>

    </article>
    """


# --------------------------------------
# 7. Collect all news
# --------------------------------------

singapore = fetch_recent_stories(
    FEEDS["Singapore Headlines"]
)

financial = fetch_recent_stories(
    FEEDS["Financial Updates"]
)

global_news = fetch_recent_stories(
    FEEDS["Global Markets"]
)


# --------------------------------------
# 8. Turn lists into HTML
# --------------------------------------

def render_list(stories):

    if not stories:

        return """
        <p class="empty">
            No qualifying stories were found
            from the selected feeds in the
            last 24 hours.
        </p>
        """

    result = ""

    for number, story in enumerate(
        stories,
        start=1
    ):

        result += make_story_html(
            story,
            number
        )

    return result


singapore_html = render_list(
    singapore
)

financial_html = render_list(
    financial
)

global_html = render_list(
    global_news
)


# --------------------------------------
# 9. Thought of the Day
# --------------------------------------
#
# Without AI, keep a list of pre-written
# compliant thoughts.
# Python chooses one each day.
# --------------------------------------

THOUGHTS = [

    "Markets change daily. A long-term financial plan should be built around your goals, time horizon and ability to manage risk.",

    "A diversified portfolio cannot remove risk, but it can help avoid relying too heavily on one market, sector or investment.",

    "Short-term headlines can be noisy. Your financial decisions should still begin with your goals and time horizon.",

    "Successful long-term planning is often less about predicting tomorrow and more about preparing for different possibilities.",

    "Consistency can matter more than trying to perfectly time every market movement."
]


thought = THOUGHTS[
    now_sg.toordinal() % len(THOUGHTS)
]


# --------------------------------------
# 10. Build complete HTML page
# --------------------------------------

page = f"""<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>
BuildWithJam Daily Market Brief
</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{

    margin: 0;

    font-family:
    Arial,
    Helvetica,
    sans-serif;

    background:
    #FBF8FD;

    color:
    #1F2A44;
}}

.container {{

    max-width: 1200px;

    margin: auto;

    background:
    white;

}}

.hero {{

    padding:
    45px;

    background:
    #FFF7E6;

}}

.morning {{

    display:
    inline-block;

    background:
    #D9A441;

    padding:
    10px 18px;

    border-radius:
    10px;

    font-weight:
    bold;

}}

h1 {{

    color:
    #5B2C83;

    font-size:
    48px;

    margin-bottom:
    10px;

}}

.date {{

    font-weight:
    bold;

    color:
    #3E1E5F;

}}

.nav {{

    display:
    grid;

    grid-template-columns:
    repeat(4, 1fr);

    background:
    #5B2C83;

}}

.nav a {{

    padding:
    18px;

    color:
    white;

    text-decoration:
    none;

    text-align:
    center;

    font-weight:
    bold;

}}

.nav a:hover {{

    background:
    #3E1E5F;

}}

.columns {{

    display:
    grid;

    grid-template-columns:
    repeat(3, 1fr);

    gap:
    16px;

    padding:
    20px;

}}

.column {{

    border:
    1px solid #E6DCEF;

    border-radius:
    12px;

    overflow:
    hidden;

}}

.column-title {{

    padding:
    16px;

    color:
    white;

    font-weight:
    bold;

}}

.sg-title {{

    background:
    #5B2C83;

}}

.fin-title {{

    background:
    #23843B;

}}

.global-title {{

    background:
    #7244AA;

}}

.story {{

    display:
    flex;

    gap:
    12px;

    padding:
    18px;

    border-bottom:
    1px solid #E6DCEF;

}}

.number {{

    width:
    32px;

    height:
    32px;

    border-radius:
    50%;

    background:
    #D9A441;

    display:
    flex;

    align-items:
    center;

    justify-content:
    center;

    font-weight:
    bold;

}}

.story h3 {{

    margin-top:
    0;

    font-size:
    17px;

}}

.story a {{

    color:
    #3E1E5F;

}}

.summary {{

    font-size:
    14px;

    line-height:
    1.5;

}}

.source {{

    margin-top:
    10px;

    color:
    #6B7280;

    font-size:
    12px;

}}

.empty {{

    padding:
    20px;

    color:
    #6B7280;

}}

.thought {{

    margin:
    20px;

    padding:
    25px;

    background:
    #FFF7E6;

    border:
    1px solid #D9A441;

    border-radius:
    12px;

    text-align:
    center;

}}

.thought h2 {{

    color:
    #5B2C83;

}}

.whatsapp {{

    background:
    #3E1E5F;

    padding:
    25px;

    text-align:
    center;

    color:
    white;

}}

.whatsapp a {{

    display:
    inline-block;

    background:
    #23843B;

    color:
    white;

    padding:
    14px 22px;

    margin-top:
    10px;

    border-radius:
    8px;

    text-decoration:
    none;

    font-weight:
    bold;

}}

footer {{

    padding:
    25px;

    background:
    #1F2A44;

    color:
    white;

    font-size:
    12px;

    line-height:
    1.6;

}}

.brand {{

    color:
    #D9A441;

    font-size:
    19px;

    font-weight:
    bold;

}}

@media
(max-width: 800px) {{

    .columns {{

        grid-template-columns:
        1fr;

    }}

    .nav {{

        grid-template-columns:
        1fr;

    }}

    h1 {{

        font-size:
        35px;

    }}

}}

</style>

</head>


<body>


<div class="container">


<header class="hero">

<div class="morning">
☀ MORNING BRIEF
</div>

<h1>
DAILY MARKET<br>
NEWS BRIEF
</h1>

<p>
Your 24-hour update on what matters
for you and your clients.
</p>

<p class="date">
📅 {today_text}
</p>

</header>


<nav class="nav">

<a href="#singapore">
🇸🇬 Singapore Headlines
</a>

<a href="#financial">
📈 Financial Updates
</a>

<a href="#global">
🌍 Global Markets
</a>

<a href="#thought">
💡 Thought of the Day
</a>

</nav>


<main class="columns">


<section
id="singapore"
class="column">

<div class="column-title sg-title">

🇸🇬 SINGAPORE HEADLINES

</div>

{singapore_html}

</section>


<section
id="financial"
class="column">

<div class="column-title fin-title">

📈 FINANCIAL UPDATES

</div>

{financial_html}

</section>


<section
id="global"
class="column">

<div class="column-title global-title">

🌍 GLOBAL MARKETS

</div>

{global_html}

</section>


</main>


<section
id="thought"
class="thought">

<h2>
💡 THOUGHT OF THE DAY
</h2>

<p>
{html.escape(thought)}
</p>

</section>


<section class="whatsapp">

<strong>

Have a question about what today's
markets could mean for your
financial plan?

</strong>

<br>

<a
href="https://wa.me/6590694815"
target="_blank"
rel="noopener noreferrer"
>

💬 WhatsApp Jamica

</a>

</section>


<footer>

<div class="brand">
#BuildWithJam
</div>

Daily Market News Brief

<br><br>

General information only.

<br>

This newsletter does not constitute
financial advice or a recommendation
to buy or sell any investment or
insurance product.

</footer>


</div>


</body>

</html>
"""


# --------------------------------------
# 11. Save page
# --------------------------------------

os.makedirs(
    "market",
    exist_ok=True
)


with open(
    "market/index.html",
    "w",
    encoding="utf-8"
) as file:

    file.write(page)


print(
    "Daily RSS market newsletter created."
)
