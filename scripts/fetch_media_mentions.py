#!/usr/bin/env python3
"""
Collects press/media mentions of Trinh Phan-Canh (in any name variant, any
language) from Google News RSS, filters out coincidental name-collision
noise (a common Vietnamese name/word), and maintains a persistent, growing
archive at _data/mediamentions.json for the /press/ Jekyll page.

Unlike NewsInSpace (a rolling window of new papers), this accumulates: press
coverage of one person is rare enough that a "last N days" window would
leave the page empty most days. Each run merges newly found items into the
existing archive rather than replacing it.
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

REQUEST_TIMEOUT = 20
OUTPUT_PATH = "_data/mediamentions.json"
MAX_ITEMS = 200

NAME_VARIANTS = ["Trinh Phan-Canh", "Phan Cảnh Trình", "Phan Canh Trinh"]

# Google News indexes journal paper pages as "articles" too, so his own
# publications keep surfacing here (they already have a home on /papers/).
# Exclude known scholarly publisher/journal brands by source name so this
# page stays actual third-party press coverage, not a duplicate paper list.
PUBLISHER_SOURCES = [
    "nature", "cell press", "cell reports", "cell ", "science", "sciencedirect",
    "asm journals", "plos", "wiley", "springer", "elsevier", "frontiers",
    "oxford academic", "taylor & francis", "biorxiv", "medrxiv", "pnas",
    "jama", "the lancet", "bmj", "acs publications", "onlinelibrary",
    "journals.asm.org", "pubmed", "europe pmc",
]

LOCALES = [
    ("en-US", "US", "US:en"),
    ("vi-VN", "VN", "VN:vi"),
    ("de-AT", "AT", "AT:de"),
]

# An article must mention the person's name (via the search query itself)
# AND at least one of these, so a common Vietnamese name/word colliding with
# an unrelated article (a movie, a celebrity, travel news, ...) gets rejected.
CONTEXT_KEYWORDS = [
    "candida", "auris", "fungal", "fungus", "nấm", "antifungal", "kháng nấm",
    "kháng thuốc", "microbio", "vi sinh vật", "nature microbiology", "cell reports",
    "nature ", "science", "cancer discovery", "vienna", "harvard", "bidmc",
    "kuchler", "meduni", "max perutz", "phd", "tiến sĩ", "postdoc",
    "pharmacist", "dược sĩ", "award", "giải thưởng khoa học", "prize",
    "gương mặt trẻ", "dermatology", "skin", "làn da",
    "spatial multiomics", "spatial biology",
]
# Deliberately excludes short/generic terms that cause false positives:
# "da" alone (substring-matches "Prada", "danh", etc.) and bare
# "nghiên cứu"/"researcher"/"nhà khoa học" (match nearly any science
# article regardless of whether it's actually about this specific person).


def http_get_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; InTheNewsBot/1.0)"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_rss_items(xml_text):
    items = []
    for block in re.findall(r"<item>(.*?)</item>", xml_text, re.DOTALL):
        def field(tag, attr_pattern=None):
            m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", block, re.DOTALL)
            return m.group(1).strip() if m else ""

        title = field("title")
        link = field("link")
        pub_date = field("pubDate")
        source_m = re.search(r'<source url="([^"]*)">(.*?)</source>', block)
        source_name = source_m.group(2).strip() if source_m else ""
        source_url = source_m.group(1).strip() if source_m else ""

        # Titles come as "Article Title - Source Name"; strip the duplicate suffix.
        if source_name and title.endswith(f" - {source_name}"):
            title = title[: -(len(source_name) + 3)]

        try:
            dt = parsedate_to_datetime(pub_date)
            date_iso = dt.astimezone(timezone.utc).strftime("%Y-%m-%d")
        except Exception:
            date_iso = ""

        items.append(
            {
                "title": title,
                "url": link,
                "source": source_name or source_url,
                "date": date_iso,
            }
        )
    return items


def fetch_query(name_variant, hl, gl, ceid):
    q = urllib.parse.quote(f'"{name_variant}"')
    url = f"https://news.google.com/rss/search?q={q}&hl={hl}&gl={gl}&ceid={ceid}"
    try:
        xml_text = http_get_text(url)
        return parse_rss_items(xml_text)
    except Exception as e:
        print(f"[warn] Google News fetch failed for {name_variant!r} ({hl}): {e}", file=sys.stderr)
        return []


def is_publisher_source(item):
    source = item.get("source", "").lower()
    return any(pub in source for pub in PUBLISHER_SOURCES)


def is_relevant(item):
    if is_publisher_source(item):
        return False
    blob = (item.get("title", "") + " " + item.get("source", "")).lower()
    return any(kw in blob for kw in CONTEXT_KEYWORDS)


def dedupe(items):
    seen = set()
    out = []
    for it in items:
        key = it.get("url") or it.get("title", "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out


def load_existing():
    if os.path.exists(OUTPUT_PATH):
        try:
            with open(OUTPUT_PATH) as f:
                data = json.load(f)
            return data.get("mentions", [])
        except Exception:
            return []
    return []


def main():
    print("Searching Google News for name-variant mentions...")
    candidates = []
    for name in NAME_VARIANTS:
        for hl, gl, ceid in LOCALES:
            candidates += fetch_query(name, hl, gl, ceid)

    candidates = [it for it in candidates if it.get("title") and it.get("url")]
    candidates = [it for it in candidates if is_relevant(it)]

    # Re-apply the current filter to previously saved items too, so a
    # tightened rule (e.g. a newly excluded publisher name) retroactively
    # cleans the persistent archive instead of only blocking new entries.
    existing = [it for it in load_existing() if is_relevant(it)]
    merged = dedupe(existing + candidates)
    merged.sort(key=lambda it: it.get("date", ""), reverse=True)
    merged = merged[:MAX_ITEMS]

    output = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(merged),
        "mentions": merged,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    new_count = len(merged) - len(existing)
    print(f"Wrote {len(merged)} items to {OUTPUT_PATH} ({max(new_count, 0)} new since last run)")


if __name__ == "__main__":
    main()
