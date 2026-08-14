#!/usr/bin/env python3
"""
Collects press/media mentions of Trinh Phan-Canh from public web sources, and
maintains a persistent, growing archive at _data/mediamentions.json for the
/inthenews/ Jekyll page.

Unlike NewsInSpace (a rolling window of new papers), this accumulates: press
coverage of one person is rare enough that a "last N days" window would
leave the page empty most days. Each run merges newly found items into the
existing archive rather than replacing it.

Sources:
  1. Google News RSS, searched across name variants and locales. Requires a
     science/award context keyword match to reject name-collision false
     positives (a common Vietnamese name/word), and excludes known
     scholarly publisher/journal source names so his own paper pages
     (Google indexes those as "articles" too) don't show up here duplicating
     what's already on /papers/.
  2. Altmetric's free per-paper "news" page (resolved from each paper's DOI
     via Altmetric's public redirect gateway, since the direct API now
     requires a paid key). This is far more complete than name search for
     coverage of a specific paper: dozens of outlets can pick up the same
     press release under headlines that never mention his name at all.
  3. His home institutions' own news listings (Vienna BioCenter, Max Perutz
     Labs), which Google News/Altmetric often don't index. Coverage there is
     frequently framed around the science ("Unnatural Selection") rather
     than his name, so titles/teasers are checked first and the full
     article body is fetched as a fallback. Already-checked listing URLs
     are remembered across runs so old non-matching articles aren't
     re-fetched every day.
  4. Targeted Google News searches and official RSS feeds for Vietnamese,
     Austrian/German-language, Harvard/BIDMC, and scientific-society sites.
     These searches catch smaller outlets that a general name query misses.
"""

import glob
import html
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
PAPERS_DIR = "papers/_posts"
MAX_ITEMS = 300
INSTITUTIONAL_CHECK_LIMIT = 15  # newest listing items to consider per site, per run

NAME_VARIANTS = [
    "Trinh Phan-Canh",
    "Trinh Phan Canh",
    "Trinh Phan-Can",
    "Phan Cảnh Trình",
    "Phan Canh Trinh",
]
NAME_MATCH_PATTERNS = [
    "trinh phan-canh", "trinh phan canh", "phan-canh trinh", "phan canh trinh",
    "phan cảnh trình", "trinh phan-can", "t. phan-canh", "t phan-canh",
]

GOOGLE_NAME_QUERY = "(" + " OR ".join(f'\"{name}\"' for name in NAME_VARIANTS) + ")"

# Domain-focused searches are deliberately grouped by region and language so
# Google News receives a manageable number of requests. They complement the
# broad name search; results must still pass the strict headline relevance
# check below because search indexes sometimes surface profiles or databases.
OUTLET_SEARCH_GROUPS = [
    {
        "name": "Vietnamese national outlets",
        "locale": ("vi-VN", "VN", "VN:vi"),
        "domains": [
            "tuoitre.vn", "thanhnien.vn", "vnexpress.net", "vietnamnet.vn",
            "dantri.com.vn", "tienphong.vn", "vtv.vn", "vov.vn",
            "nhandan.vn", "vietnamplus.vn", "laodong.vn", "qdnd.vn",
        ],
    },
    {
        "name": "Vietnamese science and health outlets",
        "locale": ("vi-VN", "VN", "VN:vi"),
        "domains": [
            "tiasang.com.vn", "vjst.vn", "khoahocphattrien.vn", "vista.gov.vn",
            "mst.gov.vn", "vast.gov.vn", "suckhoedoisong.vn", "baochinhphu.vn",
            "khoahoc.tv", "vnexpress.net",
        ],
    },
    {
        "name": "Austrian and German-language outlets",
        "locale": ("de-AT", "AT", "AT:de"),
        "domains": [
            "myscience.at", "science.apa.at", "apa.at", "orf.at",
            "derstandard.at", "diepresse.com", "kurier.at", "profil.at",
            "ots.at", "futurezone.at", "scilog.fwf.ac.at",
        ],
    },
    {
        "name": "Austrian institutions and life-science societies",
        "locale": ("de-AT", "AT", "AT:de"),
        "domains": [
            "meduniwien.ac.at", "viennabiocenter.org", "maxperutzlabs.ac.at",
            "oeghmp.at", "oegmbt.at", "oegmm.at", "myk.univie.ac.at",
            "univie.ac.at", "vetmeduni.ac.at", "oeaw.ac.at", "fwf.ac.at",
            "austrianbiologist.at",
        ],
    },
    {
        "name": "Harvard, BIDMC, and Boston biomedical outlets",
        "locale": ("en-US", "US", "US:en"),
        "domains": [
            "bidmc.org", "research.bidmc.org", "hms.harvard.edu",
            "news.harvard.edu", "harvard.edu", "broadinstitute.org",
            "wyss.harvard.edu", "dana-farber.org", "statnews.com",
            "bostonglobe.com",
        ],
    },
    {
        "name": "Microbiology and mycology societies",
        "locale": ("en-US", "US", "US:en"),
        "domains": [
            "microbiologysociety.org", "asm.org", "isham.org", "ecmm.info",
            "fems-microbiology.org", "dghm.org", "dgfm-ev.de", "oegmm.at",
            "oeghmp.at", "oegmbt.at",
        ],
    },
]

OFFICIAL_RSS_SOURCES = [
    ("ÖGMBT", "https://oegmbt.at/index.php/services/news/itemlist/category/31-allgemeine-news?format=feed"),
    ("Austrian Mycological Society", "https://myk.univie.ac.at/feed/"),
    ("BIDMC Core Facilities", "https://research.bidmc.org/core-facilities/news.rss"),
]

OFFICIAL_FEATURE_PAGES = [
    (
        "ÖGHMP",
        "https://www.oeghmp.at/",
        "Austrian Microbiology Prize 2026 — Trinh Phan-Canh",
    ),
]

# Google News indexes journal paper pages as "articles" too, so his own
# publications keep surfacing here (they already have a home on /papers/).
PUBLISHER_SOURCES = [
    "nature", "cell press", "cell reports", "cell ", "science", "sciencedirect",
    "asm journals", "plos", "wiley", "springer", "elsevier", "frontiers",
    "oxford academic", "taylor & francis", "biorxiv", "medrxiv", "pnas",
    "jama", "the lancet", "bmj", "acs publications", "onlinelibrary",
    "journals.asm.org", "pubmed", "europe pmc", "sti.vista.gov.vn",
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

INSTITUTIONAL_SOURCES = [
    {
        "name": "Vienna BioCenter",
        "listing_url": "https://www.viennabiocenter.org/about/news/",
        "base_url": "https://www.viennabiocenter.org",
        "item_pattern": re.compile(
            r'<a title="([^"]+)" href="(/about/news/[^"]+)">.*?datetime="([^"]*)"',
            re.DOTALL,
        ),
    },
    {
        "name": "Max Perutz Labs",
        "listing_url": "https://www.maxperutzlabs.ac.at/news/latest-news",
        "base_url": "https://www.maxperutzlabs.ac.at",
        "item_pattern": re.compile(
            r'<a href="(/news/latest-news/l/[^"]+)">\s*<h6>[^<]*</h6>\s*<p[^>]*><b>([^<]+)</b>.*?<h5>([^<]*)</h5>',
            re.DOTALL,
        ),
    },
]


def http_get_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; InTheNewsBot/1.0)"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        return resp.read().decode("utf-8", errors="replace")


def text_mentions_name(text):
    blob = text.lower()
    return any(p in blob for p in NAME_MATCH_PATTERNS)


BARE_DOMAIN_RE = re.compile(r"^https?://[^/]+/?$")


def extract_og_image(html):
    """Best-effort <meta property="og:image" content="..."> extraction.
    Attribute order varies by site, so both orderings are checked. Some
    sites default og:image to their own homepage URL when no real image
    is set -- that's not a picture, so it's rejected."""
    m = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        html, re.IGNORECASE,
    )
    if not m:
        m = re.search(
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
            html, re.IGNORECASE,
        )
    if not m:
        return None
    image_url = m.group(1)
    return None if BARE_DOMAIN_RE.match(image_url) else image_url


def fetch_og_image(url):
    """Best-effort: follow a mention's link and grab its og:image, without
    downloading or hosting the image ourselves -- we just store the
    outlet's own image URL. Any failure (dead link, bot-blocked, no
    og:image, slow host) is swallowed and simply means no thumbnail;
    links naturally go stale over time and that's fine."""
    if not url:
        return None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; InTheNewsBot/1.0)"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read(400_000).decode("utf-8", errors="replace")
        return extract_og_image(html)
    except Exception:
        return None


def resolve_google_news_url(redirect_url):
    """Google News RSS links (the CBMi... tokens) aren't real redirects --
    the destination is only resolvable via Google's internal batchexecute
    endpoint (reverse-engineered, undocumented, and could break if Google
    changes it -- fails silently like everything else here). Only used to
    find an og:image; the RSS link shown to visitors is left untouched."""
    try:
        page_html = http_get_text(redirect_url)
        id_m = re.search(r'data-n-a-id="([^"]+)"', page_html)
        sg_m = re.search(r'data-n-a-sg="([^"]+)"', page_html)
        ts_m = re.search(r'data-n-a-ts="([^"]+)"', page_html)
        if not (id_m and sg_m and ts_m):
            return None

        inner = json.dumps([
            "garturlreq",
            [["X", "X", ["X", "X"], None, None, 1, 1, "US:en", None, 1,
              None, None, None, None, None, 0, 1],
             "X", "X", 1, [1, 1, 1], 1, 1, None, 0, 0, None, 0],
            id_m.group(1), int(ts_m.group(1)), sg_m.group(1),
        ])
        freq = json.dumps([[["Fbv4je", inner, None, "generic"]]])
        data = urllib.parse.urlencode({"f.req": freq}).encode()
        req = urllib.request.Request(
            "https://news.google.com/_/DotsSplashUi/data/batchexecute?rpcids=Fbv4je",
            data=data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "User-Agent": "Mozilla/5.0 (compatible; InTheNewsBot/1.0)",
            },
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            body = resp.read().decode("utf-8", errors="replace")
        # The URL sits inside a JSON-encoded string nested in the outer
        # response, so its quotes come through backslash-escaped.
        m = re.search(r'garturlres\\?",\\?"(https?://[^"\\]+)', body)
        return m.group(1) if m else None
    except Exception:
        return None


def image_for_mention(via, url):
    """Dispatches to the right resolution path per source before grabbing
    an og:image; still just a best-effort link, never downloaded."""
    if via == "google_news":
        real_url = resolve_google_news_url(url)
        return fetch_og_image(real_url) if real_url else None
    return fetch_og_image(url)


# --- Source 1: Google News RSS -------------------------------------------

def parse_rss_items(xml_text):
    items = []
    for block in re.findall(r"<item>(.*?)</item>", xml_text, re.DOTALL):
        def field(tag):
            m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", block, re.DOTALL)
            return m.group(1).strip() if m else ""

        title = html.unescape(re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", field("title"), flags=re.DOTALL))
        link = html.unescape(field("link"))
        pub_date = field("pubDate")
        source_m = re.search(r'<source url="([^"]*)">(.*?)</source>', block)
        source_name = html.unescape(source_m.group(2).strip()) if source_m else ""
        source_url = source_m.group(1).strip() if source_m else ""

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
                "via": "google_news",
            }
        )
    return items


def fetch_google_news():
    print("[google_news] searching broad and outlet-targeted name queries...")
    candidates = []
    queries = [(GOOGLE_NAME_QUERY, locale, "broad") for locale in LOCALES]
    for group in OUTLET_SEARCH_GROUPS:
        site_clause = " OR ".join(f"site:{domain}" for domain in group["domains"])
        queries.append((
            f"{GOOGLE_NAME_QUERY} ({site_clause})",
            group["locale"],
            group["name"],
        ))

    for query, (hl, gl, ceid), label in queries:
        params = urllib.parse.urlencode({"q": query, "hl": hl, "gl": gl, "ceid": ceid})
        url = "https://news.google.com/rss/search?" + params
        try:
            found = parse_rss_items(http_get_text(url))
            candidates += found
            print(f"[google_news] {label}: {len(found)} result(s)")
        except Exception as e:
            print(f"[warn][google_news] fetch failed for {label!r} ({hl}): {e}", file=sys.stderr)

    def is_publisher_source(item):
        source = item.get("source", "").lower()
        return any(pub in source for pub in PUBLISHER_SOURCES)

    def is_relevant(item):
        if is_publisher_source(item):
            return False
        title = item.get("title", "")
        title_blob = title.lower()
        # Search engines can return directory/profile pages whose site name
        # happens to contain a science keyword. Requiring the headline itself
        # to carry the person's name or a relevant context keeps those out.
        return text_mentions_name(title) or any(kw in title_blob for kw in CONTEXT_KEYWORDS)

    candidates = [it for it in candidates if it.get("title") and it.get("url")]
    # The same article often appears in several locale and outlet queries.
    # Deduplicate before resolving thumbnails, which is the expensive step.
    relevant = dedupe([it for it in candidates if is_relevant(it)])
    for it in relevant:
        it["image"] = image_for_mention("google_news", it["url"])
    return relevant


def fetch_official_feeds():
    """Check official society/institution RSS plus a small number of pages."""
    candidates = []
    for source_name, url in OFFICIAL_RSS_SOURCES:
        print(f"[official_feed] checking {source_name}...")
        try:
            xml = http_get_text(url)
        except Exception as e:
            print(f"[warn][official_feed] fetch failed for {source_name}: {e}", file=sys.stderr)
            continue
        for block in re.findall(r"<item>(.*?)</item>", xml, re.DOTALL):
            def field(tag):
                match = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", block, re.DOTALL)
                return match.group(1).strip() if match else ""

            title = html.unescape(re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", field("title"), flags=re.DOTALL))
            description = html.unescape(re.sub(r"<[^>]+>", " ", field("description")))
            if not text_mentions_name(title + " " + description):
                continue
            link = html.unescape(field("link"))
            try:
                date_iso = parsedate_to_datetime(field("pubDate")).astimezone(timezone.utc).strftime("%Y-%m-%d")
            except Exception:
                date_iso = ""
            candidates.append({
                "title": re.sub(r"<[^>]+>", "", title).strip(),
                "url": link or url,
                "source": source_name,
                "date": date_iso,
                "via": "institutional",
                "image": fetch_og_image(link),
            })

    for source_name, url, mention_title in OFFICIAL_FEATURE_PAGES:
        print(f"[official_page] checking {source_name}...")
        try:
            page_html = http_get_text(url)
        except Exception as e:
            print(f"[warn][official_page] fetch failed for {source_name}: {e}", file=sys.stderr)
            continue
        if text_mentions_name(re.sub(r"<[^>]+>", " ", page_html)):
            candidates.append({
                "title": mention_title,
                "url": url,
                "source": source_name,
                "date": "",
                "via": "institutional",
                "image": extract_og_image(page_html),
            })
    return candidates


# --- Source 2: Altmetric per-paper news -----------------------------------

def get_paper_dois():
    dois = []
    for path in glob.glob(os.path.join(PAPERS_DIR, "*.md")):
        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
            m = re.search(r"^doi:\s*(\S+)\s*$", content, re.MULTILINE)
            if m:
                dois.append(m.group(1).strip())
        except Exception:
            continue
    return sorted(set(dois))


def resolve_altmetric_id(doi):
    url = f"https://www.altmetric.com/details.php?doi={urllib.parse.quote(doi)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            final_url = resp.geturl()
        m = re.search(r"/details/(\d+)", final_url)
        return m.group(1) if m else None
    except Exception:
        return None


def fetch_altmetric_news(altmetric_id, paper_title):
    url = f"https://nature.altmetric.com/details/{altmetric_id}/news"
    try:
        page_html = http_get_text(url)
    except Exception as e:
        print(f"[warn][altmetric] news fetch failed for id {altmetric_id}: {e}", file=sys.stderr)
        return []

    items = []
    for block in re.findall(r"<article class=\"post[^\"]*\">(.*?)</article>", page_html, re.DOTALL):
        title_m = re.search(r"<h3>(.*?)</h3>", block, re.DOTALL)
        source_m = re.search(r'alt="([^"]+)"', block)
        date_m = re.search(r'datetime="([^"]*)"', block)
        href_m = re.search(r'<a[^>]+class="block_link"[^>]+href="([^"]+)"', block)

        if not title_m or not source_m:
            continue

        title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip()
        title = title.replace("&#39;", "'").replace("&amp;", "&").replace("&quot;", '"')
        source = source_m.group(1).strip()
        date_iso = ""
        if date_m and date_m.group(1):
            try:
                date_iso = date_m.group(1)[:10]
            except Exception:
                pass
        link = html.unescape(href_m.group(1)) if href_m else url  # fall back to the Altmetric page itself

        items.append(
            {
                "title": title or f"Coverage of: {paper_title}",
                "url": link,
                "source": source,
                "date": date_iso,
                "via": "altmetric",
                "image": fetch_og_image(link),
            }
        )
    return items


def fetch_altmetric_sources():
    dois = get_paper_dois()
    print(f"[altmetric] checking {len(dois)} papers for news coverage...")
    candidates = []
    for doi in dois:
        altmetric_id = resolve_altmetric_id(doi)
        if not altmetric_id:
            continue
        candidates += fetch_altmetric_news(altmetric_id, doi)
    return candidates


# --- Source 3: Institutional news listings ---------------------------------

def fetch_institutional_sources(already_checked):
    candidates = []
    newly_checked = set()

    for site in INSTITUTIONAL_SOURCES:
        print(f"[institutional] checking {site['name']}...")
        try:
            html = http_get_text(site["listing_url"])
        except Exception as e:
            print(f"[warn][institutional] listing fetch failed for {site['name']}: {e}", file=sys.stderr)
            continue

        matches = site["item_pattern"].findall(html)[:INSTITUTIONAL_CHECK_LIMIT]
        for match in matches:
            if site["name"] == "Vienna BioCenter":
                title, href, date_raw = match
            else:
                href, title, date_raw = match

            full_url = site["base_url"] + href
            if full_url in already_checked:
                continue
            newly_checked.add(full_url)

            date_iso = ""
            m = re.search(r"\d{4}-\d{2}-\d{2}", date_raw)
            if m:
                date_iso = m.group(0)

            title_clean = re.sub(r"<[^>]+>", "", title).strip()

            # Titles are often topic-based ("Unnatural Selection") rather
            # than name-based, so check the title first and fall back to
            # fetching the full article body.
            found_in_title = text_mentions_name(title_clean)
            found_in_body = False
            article_html = None
            if not found_in_title:
                try:
                    article_html = http_get_text(site["base_url"] + href)
                    body_text = re.sub(r"<[^>]+>", " ", article_html)
                    found_in_body = text_mentions_name(body_text)
                except Exception as e:
                    print(f"[warn][institutional] article fetch failed for {full_url}: {e}", file=sys.stderr)

            if found_in_title or found_in_body:
                # Fetch the article page for its hero image if we don't
                # already have it from the name-matching fallback above.
                if article_html is None:
                    try:
                        article_html = http_get_text(site["base_url"] + href)
                    except Exception as e:
                        print(f"[warn][institutional] article fetch failed for {full_url}: {e}", file=sys.stderr)

                image = extract_og_image(article_html) if article_html else None

                candidates.append(
                    {
                        "title": title_clean,
                        "url": full_url,
                        "source": site["name"],
                        "date": date_iso,
                        "via": "institutional",
                        "image": image,
                    }
                )

    return candidates, newly_checked


# --- Merge & persist --------------------------------------------------------

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


def load_existing_state():
    if os.path.exists(OUTPUT_PATH):
        try:
            with open(OUTPUT_PATH) as f:
                data = json.load(f)
            return data.get("mentions", []), set(data.get("checked_institutional_urls", []))
        except Exception:
            return [], set()
    return [], set()


def is_google_news_still_valid(item):
    """Re-applies the Google News publisher/context filter to previously
    saved Google-News-sourced items, so a tightened rule retroactively
    cleans the archive. Non-Google-News items are always kept."""
    if item.get("via") != "google_news":
        return True
    source = item.get("source", "").lower()
    if any(pub in source for pub in PUBLISHER_SOURCES):
        return False
    title = item.get("title", "")
    title_blob = title.lower()
    return text_mentions_name(title) or any(kw in title_blob for kw in CONTEXT_KEYWORDS)


def backfill_images(items):
    """One-time, per-item: older archive entries collected before image
    support existed won't have an "image" key at all. Attempt it once and
    record the outcome (even None) so we don't keep re-fetching a
    permanently-dead link on every future run."""
    for it in items:
        if "image" in it:
            continue
        if it.get("via") in ("google_news", "altmetric", "manual_seed"):
            it["image"] = image_for_mention(it.get("via"), it.get("url"))
    return items


def main():
    existing, checked_urls = load_existing_state()
    existing = [it for it in existing if is_google_news_still_valid(it)]
    existing = backfill_images(existing)

    google_items = fetch_google_news()
    altmetric_items = fetch_altmetric_sources()
    institutional_items, newly_checked = fetch_institutional_sources(checked_urls)
    official_feed_items = fetch_official_feeds()
    checked_urls |= newly_checked

    all_new = google_items + altmetric_items + institutional_items + official_feed_items
    # Prefer freshly fetched metadata for a URL (corrected titles, images, or
    # source labels), then retain every older archive-only mention.
    merged = dedupe(all_new + existing)
    merged.sort(key=lambda it: it.get("date", ""), reverse=True)
    merged = merged[:MAX_ITEMS]

    output = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(merged),
        "outlet_domains_checked": sum(len(group["domains"]) for group in OUTLET_SEARCH_GROUPS),
        "mentions": merged,
        "checked_institutional_urls": sorted(checked_urls),
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    new_count = len(merged) - len(existing)
    print(f"Wrote {len(merged)} items to {OUTPUT_PATH} ({max(new_count, 0)} new since last run)")


if __name__ == "__main__":
    main()
