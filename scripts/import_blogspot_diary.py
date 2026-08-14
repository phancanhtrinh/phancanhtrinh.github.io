#!/usr/bin/env python3
"""Import the public Blogspot archive into the Jekyll diary collection."""

from __future__ import annotations

import html
import json
import re
import shutil
import urllib.request
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET


BLOG_FEED = "https://phancanhtrinh.blogspot.com/feeds/posts/default?alt=json&max-results=500"
ROOT = Path(__file__).resolve().parents[1]
DIARY_DIR = ROOT / "_diary"


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "entry"


def clean_html(raw: str) -> str:
    raw = html.unescape(raw)
    raw = re.sub(r"(?is)<(script|style|iframe|object|embed)[^>]*>.*?</\1>", "", raw)
    raw = re.sub(r"(?is)<noscript[^>]*>.*?</noscript>", "", raw)
    raw = raw.replace('target="_blank"', 'target="_blank" rel="noopener"')
    return raw.strip()


def fetch_feed() -> dict:
    with urllib.request.urlopen(BLOG_FEED) as response:
        return json.load(response)


def extract_content(entry: dict) -> str:
    content = entry.get("content", {}).get("$t") or entry.get("summary", {}).get("$t") or ""
    return clean_html(content)


def entry_date(entry: dict) -> datetime:
    published = entry.get("published", {}).get("$t") or entry.get("updated", {}).get("$t")
    return datetime.fromisoformat(published.replace("Z", "+00:00"))


def entry_permalink(entry: dict) -> str:
    for link in entry.get("link", []):
        if link.get("rel") == "alternate":
            return link.get("href", "")
    return ""


def make_front_matter(title: str, date: datetime, permalink: str, source_url: str) -> str:
    return "\n".join(
        [
            "---",
            "layout: post",
            f"title: {title!r}",
            f"date: {date.isoformat()}",
            "categories:",
            "  - diary",
            f"permalink: {permalink}",
            f"source_url: {source_url}",
            "---",
            "",
        ]
    )


def main() -> None:
    data = fetch_feed()
    entries = data.get("feed", {}).get("entry", [])
    DIARY_DIR.mkdir(exist_ok=True)

    for old_path in DIARY_DIR.glob("*"):
        if old_path.is_file():
            old_path.unlink()
        elif old_path.is_dir():
            shutil.rmtree(old_path)

    for entry in entries:
        title = entry.get("title", {}).get("$t", "Untitled")
        date = entry_date(entry)
        slug = slugify(title)
        filename = f"{date:%Y-%m-%d}-{slug}.md"
        content = extract_content(entry)
        source_url = entry_permalink(entry)
        permalink = f"/diary/{date:%Y/%m/%d}/{slug}/"
        body = make_front_matter(title, date, permalink, source_url) + content + "\n"
        (DIARY_DIR / filename).write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()
