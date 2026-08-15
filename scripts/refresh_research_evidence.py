#!/usr/bin/env python3
"""Refresh the public evidence index from the site's paper and media records."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "research-evidence.md"
MEDIA = ROOT / "_data" / "mediamentions.json"


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def main() -> None:
    text = EVIDENCE.read_text(encoding="utf-8")
    mentions = json.loads(MEDIA.read_text(encoding="utf-8")).get("mentions", []) if MEDIA.exists() else []
    lines = ["## Recent monitored updates", "", "This section is refreshed automatically from the website's monitored media index. Each item must be verified at its original outlet before being used as a factual claim.", ""]
    relevant = [item for item in mentions if re.search(r"trinh|phan-canh|candida auris|austrian microbiology prize|young investigator", clean(item.get("title")).lower())]
    for item in relevant[:12]:
        title, source, published, url = (clean(item.get(key)) for key in ("title", "source", "date", "url"))
        if title and url:
            lines.append(f"- {title} — {source or 'public outlet'}, {published or 'date not listed'}: {url}")
    block = "\n".join(lines).rstrip() + "\n"
    pattern = r"\n## Recent monitored updates\n.*?(?=\n## |\Z)"
    if re.search(pattern, text, flags=re.S):
        text = re.sub(pattern, "\n" + block, text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + block
    text = re.sub(r"Last reviewed: \d{1,2} \w+ \d{4}", f"Last reviewed: {date.today().strftime('%d %B %Y')}", text)
    EVIDENCE.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
