#!/usr/bin/env python3
"""
Fetches recent life-science papers with priority given to spatial biology,
synthetic biology, cancer biology, AI-driven biology, immunology, organoids,
organ-on-a-chip, and host-pathogen interactions from:
  - Europe PMC (covers Nature-, Cell-, Science-family journals, and Cancer Discovery)
  - bioRxiv (preprints)
  - arXiv (preprints, q-bio / cs.AI / cs.LG categories)

Writes results to _data/newsinspace.json for the /newsinspace/ Jekyll page.
Each run queries a rolling recent window, so the output is always a fresh
snapshot rather than an ever-growing archive.
"""

import json
import html
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone

WINDOW_DAYS = 14          # how far back to search
MAX_JOURNAL_ITEMS = 100   # flagship papers plus spatially weighted family journals
MAX_PREPRINT_ITEMS = 40   # cap for bioRxiv + arXiv combined
MAX_NEW_SUMMARIES = 20    # keep daily AI usage predictable
REQUEST_TIMEOUT = 30
OUTPUT_PATH = "_data/newsinspace.json"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
SUMMARY_PROMPT = (
    "Summarize this paper's key finding as 2-3 short bullet points (take-home "
    "message for a fellow researcher skimming a feed, each bullet under ~20 "
    "words). Return ONLY the bullets, one per line, each starting with \"- \". "
    "No preamble, no closing remarks.\n\nTitle: {title}\n\nAbstract: {abstract}"
)
HEADLINE_PROMPT = (
    "Write one concise headline-style takeaway for a life-science researcher, "
    "using ONLY what is explicitly stated in the paper title below. Do not "
    "invent a result, mechanism, direction, or significance. Return exactly "
    "one line starting with \"- \" and keep it under 22 words.\n\nTitle: {title}"
)

SPATIAL_PHRASES = [
    "spatial multiomics", "spatial multi-omics", "spatial transcriptomics",
    "spatial proteomics", "spatial genomics", "spatial omics",
    "spatial biology", "spatial atlas", "in situ sequencing",
    "imaging mass cytometry", "MERFISH", "CosMx", "Xenium", "Visium",
    "CODEX", "MIBI", "spatially resolved", "single-cell spatial",
    "multiplexed imaging", "tissue architecture", "spatial organization",
    "cell localization", "cell atlas", "single-cell atlas", "3D genome",
]

SYNTHETIC_BIOLOGY_PHRASES = [
    "synthetic biology", "synthetic circuit", "gene circuit",
    "cell engineering", "engineered cell", "genome engineering",
    "gene editing", "genome editing", "CRISPR", "base editing",
    "prime editing", "protein design", "directed evolution",
]

FOCUS_PHRASES = [
    "oncovirus", "oncogenic virus", "viral oncogenesis",
    "virus-associated cancer", "virus-induced cancer",
    "HPV-associated cancer", "EBV-associated cancer",
    "spatial biotechnology", "single-cell", "single cell", "multiomics",
    "multi-omics", "systems biology", "computational biology",
    "artificial intelligence", "machine learning", "deep learning",
    "foundation model", "large language model",
    "immunology", "immune response", "immune cell",
    "organoid", "organoids",
    "organ-on-a-chip", "organ-on-chip", "organs-on-chips",
    "microphysiological system",
    "host-pathogen interaction", "host-pathogen interactions",
    "host pathogen interaction",
]

CANCER_KEYWORDS_LOWER = ["cancer", "tumor", "tumour", "oncogen", "carcinoma", "malignan"]
LIFE_SCIENCE_KEYWORDS_LOWER = [
    "cell", "protein", "rna", "dna", "gene", "genom", "immune", "tissue",
    "disease", "biolog", "molecular", "microb", "bacter", "virus", "brain",
    "neural", "clinical", "patient", "human", "mouse", "stem", "metabol",
    "organoid", "development", "physiolog", "drug", "therap", "vaccine",
]
EXCLUDED_TITLE_PREFIXES = (
    "author correction", "publisher correction", "correction:",
    "retraction notice", "retracted:",
)

SPATIAL_KEYWORDS_LOWER = [p.lower() for p in SPATIAL_PHRASES]
SYNTHETIC_KEYWORDS_LOWER = [p.lower() for p in SYNTHETIC_BIOLOGY_PHRASES]
FOCUS_KEYWORDS_LOWER = [p.lower() for p in FOCUS_PHRASES]
TOPIC_PRIORITY = {"spatial": 4, "synthetic": 3, "focus": 2, "life-science": 1}

CELL_PRESS_JOURNALS = (
    "Cell", "Cancer Cell", "Immunity", "Molecular Cell", "Neuron",
    "Developmental Cell", "Current Biology", "Cell Host & Microbe",
    "Cell Metabolism", "Cell Stem Cell", "Cell Chemical Biology",
    "Cell Systems", "Cell Genomics", "Cell Reports", "Cell Reports Medicine",
    "Cell Reports Methods", "iScience", "Med", "Trends in Cancer",
    "Trends in Immunology", "Trends in Biotechnology",
)
SCIENCE_JOURNALS = (
    "Science", "Science Advances", "Science Immunology",
    "Science Translational Medicine", "Science Signaling", "Science Robotics",
)
EUROPEPMC_JOURNAL_QUERIES = {
    "nature": "JOURNAL:Nature*",
    "cell": " OR ".join(f'JOURNAL:"{name}"' for name in CELL_PRESS_JOURNALS),
    "science": " OR ".join(f'JOURNAL:"{name}"' for name in SCIENCE_JOURNALS),
    "cancer-discovery": 'JOURNAL:"Cancer Discovery"',
}

BIORXIV_CATEGORIES = (
    "cancer biology", "bioinformatics", "systems biology", "genomics",
    "synthetic biology", "cell biology", "genetics", "immunology",
    "molecular biology", "microbiology", "bioengineering",
    "developmental biology",
)

# Restricted to q-bio.* so results stay biology-scoped: arXiv's cs.AI/cs.LG
# categories are dominated by generic ML papers that happen to mention
# "machine learning" without being biology papers at all.
ARXIV_CATEGORIES = ["q-bio.QM", "q-bio.GN", "q-bio.CB", "q-bio.TO", "q-bio.MN"]


def http_get_json(url, headers=None):
    req = urllib.request.Request(
        url, headers=headers or {"User-Agent": "NewsInSpace/1.0"}
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            retryable = not isinstance(e, urllib.error.HTTPError) or e.code == 429 or e.code >= 500
            if attempt == 2 or not retryable:
                raise
            time.sleep(2 ** attempt)


def classify_topic(*texts):
    blob = " ".join(t for t in texts if t).lower()
    if any(kw in blob for kw in SPATIAL_KEYWORDS_LOWER):
        return "spatial"
    if any(kw in blob for kw in SYNTHETIC_KEYWORDS_LOWER):
        return "synthetic"
    if any(kw in blob for kw in FOCUS_KEYWORDS_LOWER + CANCER_KEYWORDS_LOWER):
        return "focus"
    return "life-science"


def looks_like_life_science(*texts):
    blob = " ".join(t for t in texts if t).lower()
    return classify_topic(blob) != "life-science" or any(
        keyword in blob for keyword in LIFE_SCIENCE_KEYWORDS_LOWER
    )


def is_eligible_item(item):
    title = item.get("title", "").strip().lower()
    return bool(title) and not title.startswith(EXCLUDED_TITLE_PREFIXES)


def normalize_journal_name(name):
    return " ".join((name or "").lower().replace(".", "").split())


def is_flagship_journal(name):
    normalized = normalize_journal_name(name)
    return (
        normalized in {"nature", "cell", "science"}
        or normalized.startswith("science (")
    )


def fetch_europepmc(start_date, end_date):
    """Recent Nature, Cell, and Science-family records from Europe PMC."""
    def fetch_family(family, journal_query):
        query = f"({journal_query}) AND FIRST_PDATE:[{start_date} TO {end_date}]"
        params = {
            "query": query,
            "format": "json",
            "resultType": "core",
            "pageSize": "1000",
            "sort": "P_PDATE_D desc",
        }
        url = (
            "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
            + urllib.parse.urlencode(params)
        )
        data = http_get_json(url)
        family_items = []
        for r in data.get("resultList", {}).get("result", []):
            doi = r.get("doi")
            url_out = f"https://doi.org/{doi}" if doi else r.get("fullTextUrlList", {}).get(
                "fullTextUrl", [{}]
            )[0].get("url", "")
            item = {
                    "title": r.get("title", "").rstrip("."),
                    "authors": r.get("authorString", ""),
                    "journal": r.get("journalInfo", {}).get("journal", {}).get("title", r.get("source", "")),
                    "date": r.get("firstPublicationDate", ""),
                    "url": url_out,
                    "doi": doi or "",
                    "abstract": (r.get("abstractText") or "")[:400],
                    "source": "journal",
                    "journal_family": family,
                }
            item["topic"] = classify_topic(item["title"], item["abstract"])
            item["flagship"] = is_flagship_journal(item["journal"])
            if looks_like_life_science(item["title"], item["abstract"]):
                family_items.append(item)
        return family_items

    items = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            pool.submit(fetch_family, family, query): family
            for family, query in EUROPEPMC_JOURNAL_QUERIES.items()
        }
        for future in as_completed(futures):
            family = futures[future]
            try:
                family_items = future.result()
                items.extend(family_items)
                print(f"[Europe PMC] {family}: {len(family_items)} life-science item(s)")
            except Exception as e:
                print(f"[warn] Europe PMC {family} fetch failed: {e}", file=sys.stderr)
    return items


def fetch_biorxiv(start_date, end_date):
    """Fetch selected life-science categories concurrently.

    The official API supports a category query parameter and serves 30 results
    per page. Category-scoped requests avoid walking the entire bioRxiv catalog
    serially just to discard unrelated fields such as ecology or neuroscience.
    """
    def fetch_category(category):
        category_items = []
        cursor = 0
        while True:
            base = f"https://api.biorxiv.org/details/biorxiv/{start_date}/{end_date}/{cursor}"
            url = base + "?" + urllib.parse.urlencode({"category": category})
            data = http_get_json(url)
            collection = data.get("collection", [])
            if not collection:
                break
            for r in collection:
                title = r.get("title", "")
                abstract = r.get("abstract", "")
                doi = r.get("doi", "")
                item = {
                        "title": title.rstrip("."),
                        "authors": (r.get("authors") or "").replace(";", ","),
                        "journal": "bioRxiv (preprint)",
                        "date": r.get("date", ""),
                        "url": f"https://doi.org/{doi}" if doi else "",
                        "doi": doi,
                        "abstract": abstract[:400],
                        "source": "preprint",
                    }
                item["topic"] = classify_topic(item["title"], item["abstract"])
                category_items.append(item)
            msgs = data.get("messages", [{}])
            total = int(msgs[0].get("total", 0)) if msgs else 0
            cursor += len(collection)
            if cursor >= total:
                break
            time.sleep(0.15)
        return category_items

    items = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            pool.submit(fetch_category, category): category
            for category in BIORXIV_CATEGORIES
        }
        for future in as_completed(futures):
            category = futures[future]
            try:
                category_items = future.result()
                items.extend(category_items)
                print(f"[bioRxiv] {category}: {len(category_items)} paper(s)")
            except Exception as e:
                print(f"[warn] bioRxiv {category} fetch failed: {e}", file=sys.stderr)
    return items


def fetch_arxiv(start_date, end_date):
    items = []
    try:
        cat_clause = " OR ".join(f"cat:{c}" for c in ARXIV_CATEGORIES)
        start_fmt = start_date.replace("-", "") + "0000"
        end_fmt = end_date.replace("-", "") + "2359"
        search_query = (
            f"({cat_clause}) "
            f"AND submittedDate:[{start_fmt} TO {end_fmt}]"
        )
        params = {
            "search_query": search_query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": "200",
        }
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": "NewsInSpace/1.0"})
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            xml = resp.read().decode("utf-8")

        entries = re.findall(r"<entry>(.*?)</entry>", xml, re.DOTALL)
        for e in entries:
            def field(tag):
                m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", e, re.DOTALL)
                return (m.group(1).strip() if m else "").replace("\n", " ")

            title = re.sub(r"\s+", " ", field("title"))
            summary = re.sub(r"\s+", " ", field("summary"))
            published = field("published")[:10]
            authors = ", ".join(re.findall(r"<name>(.*?)</name>", e))
            link_m = re.search(r'<id>(.*?)</id>', e)
            link = link_m.group(1).strip() if link_m else ""
            item = {
                    "title": title,
                    "authors": authors,
                    "journal": "arXiv (preprint)",
                    "date": published,
                    "url": link,
                    "doi": "",
                    "abstract": summary[:400],
                    "source": "preprint",
                }
            item["topic"] = classify_topic(item["title"], item["abstract"])
            items.append(item)
    except Exception as e:
        print(f"[warn] arXiv fetch failed: {e}", file=sys.stderr)
    return items


def summarize_paper(title, abstract):
    """Best-effort summary, or a conservative title-only line when needed."""
    if not ANTHROPIC_API_KEY:
        return None
    try:
        has_abstract = bool(abstract and len(abstract) >= 40)
        prompt = (
            SUMMARY_PROMPT.format(title=title, abstract=abstract)
            if has_abstract
            else HEADLINE_PROMPT.format(title=title)
        )
        payload = json.dumps({
            "model": ANTHROPIC_MODEL,
            "max_tokens": 200 if has_abstract else 80,
            "messages": [
                {"role": "user", "content": prompt}
            ],
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = "".join(block.get("text", "") for block in data.get("content", []))
        bullets = [
            line.strip().lstrip("-•").strip()
            for line in text.splitlines()
            if line.strip().startswith(("-", "•"))
        ]
        return bullets[:3 if has_abstract else 1] or None
    except Exception as e:
        print(f"[warn] summarization failed for {title!r}: {e}", file=sys.stderr)
        return None


def clip_words(text, limit=28):
    words = text.split()
    if len(words) <= limit:
        return " ".join(words).rstrip(" .") + "."
    return " ".join(words[:limit]).rstrip(" ,;:.") + "…"


def fallback_summary(title, abstract):
    """Always provide three concise, source-grounded bullets when possible."""
    clean_title = html.unescape(re.sub(r"<[^>]+>", " ", title or ""))
    clean_title = re.sub(r"\s+", " ", clean_title).strip().rstrip(".")
    clean_abstract = html.unescape(re.sub(r"<[^>]+>", " ", abstract or ""))
    clean_abstract = re.sub(r"\s+", " ", clean_abstract).strip()

    if len(clean_abstract) < 40:
        return [clip_words(clean_title, 22)] if clean_title else None

    bullets = [clip_words(f"Focus: {clean_title}", 26)]
    sentences = [
        part.strip()
        for part in re.split(r"(?<=[.!?])\s+|;\s+", clean_abstract)
        if len(part.strip().split()) >= 5
    ]
    if len(sentences) >= 2:
        bullets.extend(clip_words(part) for part in sentences[:2])
    else:
        words = clean_abstract.split()
        midpoint = max(1, len(words) // 2)
        bullets.append(clip_words(" ".join(words[:midpoint])))
        bullets.append(clip_words(" ".join(words[midpoint:])))
    return bullets[:3]


def load_previous_summaries():
    """Carries forward summaries from the last run's output so unchanged
    papers (this is a rolling-window snapshot, re-fetched fresh every run,
    not an accumulating archive) aren't re-summarized -- and thus re-billed
    -- every single day for as long as they stay in the window."""
    if not os.path.exists(OUTPUT_PATH):
        return {}
    try:
        with open(OUTPUT_PATH) as f:
            data = json.load(f)
        out = {}
        for p in data.get("papers", []):
            bullets = p.get("summary_bullets")
            if bullets:
                key = p.get("doi") or p.get("title", "").strip().lower()
                out[key] = bullets
        return out
    except Exception:
        return {}


def dedupe(items):
    seen = set()
    out = []
    for it in items:
        key = it.get("doi") or it.get("title", "").strip().lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out


def item_sort_key(item):
    """Newest first, with spatial work first among papers on the same date."""
    return (item.get("date", ""), TOPIC_PRIORITY.get(item.get("topic"), 0))


def select_balanced(items, limit):
    """Reserve feed space for core topics, then backfill with recent life science.

    The quotas are ceilings, not requirements: if a lane is quiet, its unused
    space is filled by the newest papers from any lane.
    """
    candidates = dedupe([it for it in items if is_eligible_item(it)])
    candidates.sort(key=item_sort_key, reverse=True)
    quotas = {
        "spatial": limit // 2,
        "synthetic": max(4, limit // 6),
        "focus": max(6, limit // 4),
    }
    selected = []
    selected_keys = set()

    def add(item):
        key = item.get("doi") or item.get("title", "").strip().lower()
        if key in selected_keys or len(selected) >= limit:
            return
        selected.append(item)
        selected_keys.add(key)

    for topic, quota in quotas.items():
        for item in (it for it in candidates if it.get("topic") == topic):
            if sum(it.get("topic") == topic for it in selected) >= quota:
                break
            add(item)

    for item in candidates:
        add(item)

    selected.sort(key=item_sort_key, reverse=True)
    return selected


def select_journal_items(items, limit):
    """Keep every eligible flagship item, then balance the family-journal fill."""
    candidates = dedupe([it for it in items if is_eligible_item(it)])
    candidates.sort(key=item_sort_key, reverse=True)
    flagship = [it for it in candidates if it.get("flagship")]
    selected = flagship[:limit]
    selected_keys = {
        it.get("doi") or it.get("title", "").strip().lower() for it in selected
    }
    remaining = [
        it for it in candidates
        if (it.get("doi") or it.get("title", "").strip().lower()) not in selected_keys
    ]
    selected.extend(select_balanced(remaining, limit - len(selected)))
    selected.sort(key=item_sort_key, reverse=True)
    return selected


def main():
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=WINDOW_DAYS)
    start_s, end_s = start.isoformat(), end.isoformat()

    print(f"Fetching papers from {start_s} to {end_s}...")
    journal_items = select_journal_items(
        fetch_europepmc(start_s, end_s), MAX_JOURNAL_ITEMS
    )

    preprint_items = fetch_biorxiv(start_s, end_s) + fetch_arxiv(start_s, end_s)
    preprint_items = select_balanced(preprint_items, MAX_PREPRINT_ITEMS)

    all_items = dedupe(journal_items + preprint_items)
    all_items.sort(key=item_sort_key, reverse=True)

    previous_summaries = load_previous_summaries()
    new_summaries = 0
    reused_summaries = 0
    summary_attempts = 0
    # Headline-only entries are summarized first so every paper without an
    # abstract gets useful context even when the daily AI-call cap is reached.
    summary_candidates = sorted(
        all_items, key=lambda it: bool(it.get("abstract") and len(it["abstract"]) >= 40)
    )
    for it in summary_candidates:
        key = it.get("doi") or it.get("title", "").strip().lower()
        bullets = previous_summaries.get(key)
        if bullets:
            reused_summaries += 1
        elif summary_attempts < MAX_NEW_SUMMARIES:
            summary_attempts += 1
            bullets = summarize_paper(it.get("title", ""), it.get("abstract", ""))
            if bullets:
                new_summaries += 1
        fallback = fallback_summary(it.get("title", ""), it.get("abstract", ""))
        if fallback:
            if not bullets:
                bullets = fallback
            elif len(it.get("abstract", "")) >= 40 and len(bullets) < 3:
                for candidate in fallback:
                    if candidate not in bullets:
                        bullets.append(candidate)
                    if len(bullets) == 3:
                        break
        if bullets:
            it["summary_bullets"] = bullets
            it["summary_kind"] = (
                "abstract" if len(it.get("abstract", "")) >= 40 else "headline"
            )
    if ANTHROPIC_API_KEY:
        print(
            f"Summarized {new_summaries} new paper(s), reused "
            f"{reused_summaries} from the previous run"
        )
    else:
        print("[info] ANTHROPIC_API_KEY not set; using source-grounded fallback bullets")

    output = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window_days": WINDOW_DAYS,
        "count": len(all_items),
        "topic_counts": {
            topic: sum(it.get("topic") == topic for it in all_items)
            for topic in TOPIC_PRIORITY
        },
        "papers": all_items,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(all_items)} items to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
