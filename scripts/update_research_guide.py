#!/usr/bin/env python3
"""Refresh a small Claude-generated knowledge layer for the static research guide."""
from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_data" / "research_guide.json"
API = "https://api.anthropic.com/v1/messages"


def plain(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value or "")).strip()


def collect_sources() -> list[dict[str, str]]:
    sources = []
    for path in sorted((ROOT / "_posts").glob("*.md")) + sorted((ROOT / "_diary").glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        title = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', text, re.M)
        body = text.split("---", 2)[-1] if "---" in text else text
        if title:
            sources.append({"title": plain(title.group(1)), "text": plain(body)[:1200], "path": str(path.relative_to(ROOT))})
    return sources[-160:]


def main() -> None:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("ANTHROPIC_API_KEY is not set; keeping existing guide")
        return
    sources = collect_sources()
    prompt = (
        "Create a compact website knowledge layer about Trinh Phan-Canh from the supplied source records. "
        "Return ONLY valid JSON: {\"facts\":[{\"topic\":string,\"answer\":string,\"source_titles\":[string]}]}. "
        "Write 12-20 accurate, useful facts in clear English. Do not invent information; omit unsupported claims. "
        "Cover scientific contributions, Candida auris, antifungal resistance, spatial biology, career, teaching, and diary themes.\n\n"
        + json.dumps(sources, ensure_ascii=False)
    )
    payload = json.dumps({"model": "claude-haiku-4-5-20251001", "max_tokens": 5000, "messages": [{"role": "user", "content": prompt}]}).encode()
    request = urllib.request.Request(API, data=payload, headers={"content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01"})
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            result = json.load(response)
        raw = "".join(part.get("text", "") for part in result.get("content", []) if part.get("type") == "text")
        match = re.search(r"\{.*\}", raw, re.S)
        data = json.loads(match.group(0) if match else raw)
        facts = data.get("facts", [])
        if not isinstance(facts, list) or not facts:
            raise ValueError("Claude returned no facts")
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_text(json.dumps({"updated": __import__("datetime").date.today().isoformat(), "facts": facts}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Updated research guide with {len(facts)} facts")
    except Exception as exc:
        print(f"Guide refresh skipped: {exc}")


if __name__ == "__main__":
    main()
