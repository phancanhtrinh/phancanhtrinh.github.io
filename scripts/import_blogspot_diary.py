#!/usr/bin/env python3
"""Import the public Blogspot archive into the Jekyll diary collection."""

from __future__ import annotations

import html
import json
import re
import shutil
import urllib.request
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path


BLOG_FEED = "https://phancanhtrinh.blogspot.com/feeds/posts/default?alt=json&max-results=500"
ROOT = Path(__file__).resolve().parents[1]
DIARY_DIR = ROOT / "_diary"


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "entry"


class DiaryHTMLCleaner(HTMLParser):
    allowed_tags = {
        "a",
        "b",
        "blockquote",
        "br",
        "code",
        "em",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "hr",
        "img",
        "li",
        "ol",
        "p",
        "pre",
        "strong",
        "table",
        "tbody",
        "td",
        "th",
        "thead",
        "tr",
        "ul",
    }
    block_tags = {"div", "span", "font"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in self.block_tags:
            return
        if tag not in self.allowed_tags:
            return
        attrs_dict = dict(attrs)
        attrs_out = []
        if tag == "a":
            for key in ("href", "title", "target", "rel"):
                if attrs_dict.get(key):
                    attrs_out.append((key, attrs_dict[key]))
            if attrs_dict.get("target") == "_blank" and not attrs_dict.get("rel"):
                attrs_out.append(("rel", "noopener"))
        elif tag == "img":
            for key in ("src", "alt", "title", "width", "height"):
                if attrs_dict.get(key):
                    attrs_out.append((key, attrs_dict[key]))
        elif tag == "iframe":
            for key in ("src", "title", "width", "height", "allow", "allowfullscreen", "frameborder"):
                if attrs_dict.get(key):
                    attrs_out.append((key, attrs_dict[key]))
        attr_str = "".join(f' {k}="{html.escape(v, quote=True)}"' for k, v in attrs_out)
        self.parts.append(f"<{tag}{attr_str}>")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.block_tags:
            self.parts.append("\n")
            return
        if tag in self.allowed_tags and tag not in {"br", "img", "hr"}:
            self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        self.parts.append(data)

    def handle_entityref(self, name):
        self.parts.append(f"&{name};")

    def handle_charref(self, name):
        self.parts.append(f"&#{name};")

    def get_html(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
        return text.strip()


def clean_html(raw: str) -> str:
    raw = html.unescape(raw)
    raw = re.sub(r"(?is)<(script|style|object|embed)[^>]*>.*?</\1>", "", raw)
    raw = re.sub(r"(?is)<noscript[^>]*>.*?</noscript>", "", raw)
    raw = re.sub(r"(?is)<span[^>]*font-family[^>]*>", "", raw)
    raw = re.sub(r"(?is)</span>", "", raw)
    raw = re.sub(r"(?is)<font[^>]*>", "", raw)
    raw = re.sub(r"(?is)</font>", "", raw)
    raw = re.sub(r'(?is)\sstyle=(\"[^\"]*\"|\'[^\']*\'|[^\s>]+)', '', raw)
    raw = re.sub(r'(?is)\sclass=(\"[^\"]*\"|\'[^\']*\'|[^\s>]+)', '', raw)
    raw = re.sub(r'(?is)\sface=(\"[^\"]*\"|\'[^\']*\'|[^\s>]+)', '', raw)
    raw = re.sub(r"(?is)font-family\s*:\s*[^;>]+;?", "", raw)
    raw = re.sub(r"(?is)font-size\s*:\s*[^;>]+;?", "", raw)
    raw = re.sub(r"(?is)line-height\s*:\s*[^;>]+;?", "", raw)
    raw = re.sub(r"(?is)color\s*:\s*[^;>]+;?", "", raw)
    raw = raw.replace("https://www.phancanhtrinh.com", "https://phancanhtrinh.blogspot.com")
    raw = raw.replace("https://phancanhtrinh.com", "https://phancanhtrinh.blogspot.com")
    raw = raw.replace('href="/p/', 'href="https://phancanhtrinh.blogspot.com/p/')
    raw = raw.replace("<a name='more'></a>", "")
    raw = raw.replace('<a name="more"></a>', "")
    cleaner = DiaryHTMLCleaner()
    cleaner.feed(raw)
    cleaned = cleaner.get_html()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def fetch_feed() -> dict:
    with urllib.request.urlopen(BLOG_FEED) as response:
        return json.load(response)


def extract_content(entry: dict) -> str:
    content = entry.get("content", {}).get("$t") or entry.get("summary", {}).get("$t") or ""
    return clean_html(content)


def extract_excerpt(content: str) -> str:
    text = re.sub(r"(?is)<[^>]+>", " ", content)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_thumbnail(content: str) -> str:
    match = re.search(r'<img[^>]+src="([^"]+)"', content, flags=re.I)
    if match:
        return match.group(1)
    match = re.search(r"<img[^>]+src='([^']+)'", content, flags=re.I)
    if match:
        return match.group(1)
    return ""


def entry_date(entry: dict) -> datetime:
    published = entry.get("published", {}).get("$t") or entry.get("updated", {}).get("$t")
    return datetime.fromisoformat(published.replace("Z", "+00:00"))


def entry_permalink(entry: dict) -> str:
    for link in entry.get("link", []):
        if link.get("rel") == "alternate":
            return link.get("href", "")
    return ""


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def make_front_matter(
    title: str,
    date: datetime,
    permalink: str,
    source_url: str,
    summary: str = "",
    thumbnail: str = "",
) -> str:
    lines = [
        "---",
        "layout: diary_post",
        f"title: {q(title)}",
        f"date: {date.isoformat()}",
        "categories:",
        "  - diary",
        f"permalink: {permalink}",
        f"source_url: {q(source_url)}",
    ]
    if summary:
        lines.append(f"summary: {q(summary)}")
    if thumbnail:
        lines.append(f"thumbnail: {q(thumbnail)}")
    lines += [
        "---",
        "",
    ]
    return "\n".join(lines)


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
        excerpt = extract_excerpt(content)
        thumbnail = extract_thumbnail(content)
        source_url = entry_permalink(entry)
        permalink = f"/diary/{date:%Y/%m/%d}/{slug}/"
        fm = make_front_matter(
            title=title,
            date=date,
            permalink=permalink,
            source_url=source_url,
            summary=excerpt[:500] if excerpt else "",
            thumbnail=thumbnail,
        )
        body = fm + content + "\n"
        (DIARY_DIR / filename).write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()
