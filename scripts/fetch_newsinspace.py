#!/usr/bin/env python3
"""
Fetches recent papers relevant to spatial multi-omics, cancer biology,
viral-driven cancer, spatial biotechnology, and AI-driven biology from:
  - Europe PMC (covers Nature-, Cell-, Science-family journals, and Cancer Discovery)
  - bioRxiv (preprints)
  - arXiv (preprints, q-bio / cs.AI / cs.LG categories)

Writes results to _data/newsinspace.json for the /newsinspace/ Jekyll page.
Each run queries a rolling recent window, so the output is always a fresh
snapshot rather than an ever-growing archive.
"""

import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

WINDOW_DAYS = 14          # how far back to search
MAX_JOURNAL_ITEMS = 40    # cap for Nature/Cell/Science/Cancer Discovery family
MAX_PREPRINT_ITEMS = 30   # cap for bioRxiv + arXiv combined
REQUEST_TIMEOUT = 30
OUTPUT_PATH = "_data/newsinspace.json"

TOPIC_PHRASES = [
    "spatial multiomics", "spatial multi-omics", "spatial transcriptomics",
    "spatial proteomics", "spatial genomics", "spatial omics",
    "spatial biology", "spatial atlas", "in situ sequencing",
    "imaging mass cytometry", "MERFISH", "CosMx", "Xenium", "Visium",
    "oncovirus", "oncogenic virus", "viral oncogenesis",
    "virus-associated cancer", "virus-induced cancer",
    "HPV-associated cancer", "EBV-associated cancer",
    "spatial biotechnology", "single-cell spatial",
    "artificial intelligence", "machine learning", "deep learning",
    "foundation model", "large language model",
]

# Substrings used to keep/reject items after fetching, so results stay on-topic
# even where an upstream API's own search is fairly loose.
TOPIC_KEYWORDS_LOWER = [p.lower() for p in TOPIC_PHRASES]

CANCER_KEYWORDS_LOWER = ["cancer", "tumor", "tumour", "oncogen", "carcinoma", "malignan"]

EUROPEPMC_JOURNALS = [
    "Nature", "Nature Methods", "Nature Biotechnology", "Nature Medicine",
    "Nature Cancer", "Nature Communications", "Nature Genetics",
    "Nature Immunology", "Nature Cell Biology", "Nature Reviews Cancer",
    "Nature Reviews Genetics",
    "Cell", "Cell Reports", "Cancer Cell", "Immunity", "Molecular Cell",
    "Cell Genomics", "Cell Systems",
    "Science", "Science Advances", "Science Immunology",
    "Science Translational Medicine",
    "Cancer Discovery",
]

BIORXIV_CATEGORIES = {
    "cancer biology", "bioinformatics", "systems biology", "genomics",
    "synthetic biology", "cell biology", "genetics", "immunology",
    "molecular biology", "microbiology",
}

# Restricted to q-bio.* so results stay biology-scoped: arXiv's cs.AI/cs.LG
# categories are dominated by generic ML papers that happen to mention
# "machine learning" without being biology papers at all.
ARXIV_CATEGORIES = ["q-bio.QM", "q-bio.GN", "q-bio.CB", "q-bio.TO", "q-bio.MN"]


def http_get_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "NewsInSpace/1.0"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def text_matches_topics(*texts):
    blob = " ".join(t for t in texts if t).lower()
    return any(kw in blob for kw in TOPIC_KEYWORDS_LOWER) or any(
        kw in blob for kw in CANCER_KEYWORDS_LOWER
    )


def fetch_europepmc(start_date, end_date):
    """Nature/Cell/Science/Cancer Discovery family via Europe PMC metadata search."""
    journal_clause = " OR ".join(f'JOURNAL:"{j}"' for j in EUROPEPMC_JOURNALS)
    topic_clause = " OR ".join(f'"{p}"' for p in TOPIC_PHRASES)
    query = (
        f"({topic_clause}) AND ({journal_clause}) "
        f'AND FIRST_PDATE:[{start_date} TO {end_date}]'
    )
    params = {
        "query": query,
        "format": "json",
        "resultType": "core",
        "pageSize": "100",
        "sort": "P_PDATE_D desc",
    }
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(params)
    items = []
    try:
        data = http_get_json(url)
        for r in data.get("resultList", {}).get("result", []):
            doi = r.get("doi")
            url_out = f"https://doi.org/{doi}" if doi else r.get("fullTextUrlList", {}).get(
                "fullTextUrl", [{}]
            )[0].get("url", "")
            items.append(
                {
                    "title": r.get("title", "").rstrip("."),
                    "authors": r.get("authorString", ""),
                    "journal": r.get("journalInfo", {}).get("journal", {}).get("title", r.get("source", "")),
                    "date": r.get("firstPublicationDate", ""),
                    "url": url_out,
                    "doi": doi or "",
                    "abstract": (r.get("abstractText") or "")[:400],
                    "source": "journal",
                }
            )
    except Exception as e:
        print(f"[warn] Europe PMC fetch failed: {e}", file=sys.stderr)
    return items


def fetch_biorxiv(start_date, end_date):
    items = []
    cursor = 0
    try:
        while True:
            url = f"https://api.biorxiv.org/details/biorxiv/{start_date}/{end_date}/{cursor}"
            data = http_get_json(url)
            collection = data.get("collection", [])
            if not collection:
                break
            for r in collection:
                category = (r.get("category") or "").lower()
                title = r.get("title", "")
                abstract = r.get("abstract", "")
                if category not in BIORXIV_CATEGORIES:
                    continue
                if not text_matches_topics(title, abstract):
                    continue
                doi = r.get("doi", "")
                items.append(
                    {
                        "title": title.rstrip("."),
                        "authors": (r.get("authors") or "").replace(";", ","),
                        "journal": "bioRxiv (preprint)",
                        "date": r.get("date", ""),
                        "url": f"https://doi.org/{doi}" if doi else "",
                        "doi": doi,
                        "abstract": abstract[:400],
                        "source": "preprint",
                    }
                )
            msgs = data.get("messages", [{}])
            total = int(msgs[0].get("total", 0)) if msgs else 0
            cursor += 100
            if cursor >= total:
                break
            time.sleep(0.3)
    except Exception as e:
        print(f"[warn] bioRxiv fetch failed: {e}", file=sys.stderr)
    return items


def fetch_arxiv(start_date, end_date):
    items = []
    try:
        cat_clause = " OR ".join(f"cat:{c}" for c in ARXIV_CATEGORIES)
        topic_clause = " OR ".join(f'abs:"{p}"' for p in TOPIC_PHRASES)
        start_fmt = start_date.replace("-", "") + "0000"
        end_fmt = end_date.replace("-", "") + "2359"
        search_query = (
            f"({cat_clause}) AND ({topic_clause}) "
            f"AND submittedDate:[{start_fmt} TO {end_fmt}]"
        )
        params = {
            "search_query": search_query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": "50",
        }
        url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": "NewsInSpace/1.0"})
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            xml = resp.read().decode("utf-8")

        import re

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
            items.append(
                {
                    "title": title,
                    "authors": authors,
                    "journal": "arXiv (preprint)",
                    "date": published,
                    "url": link,
                    "doi": "",
                    "abstract": summary[:400],
                    "source": "preprint",
                }
            )
    except Exception as e:
        print(f"[warn] arXiv fetch failed: {e}", file=sys.stderr)
    return items


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


def main():
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=WINDOW_DAYS)
    start_s, end_s = start.isoformat(), end.isoformat()

    print(f"Fetching papers from {start_s} to {end_s}...")
    journal_items = dedupe([it for it in fetch_europepmc(start_s, end_s) if it.get("title")])
    journal_items.sort(key=lambda it: it.get("date", ""), reverse=True)
    journal_items = journal_items[:MAX_JOURNAL_ITEMS]

    preprint_items = fetch_biorxiv(start_s, end_s) + fetch_arxiv(start_s, end_s)
    preprint_items = dedupe([it for it in preprint_items if it.get("title")])
    preprint_items.sort(key=lambda it: it.get("date", ""), reverse=True)
    preprint_items = preprint_items[:MAX_PREPRINT_ITEMS]

    all_items = dedupe(journal_items + preprint_items)
    all_items.sort(key=lambda it: it.get("date", ""), reverse=True)

    output = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window_days": WINDOW_DAYS,
        "count": len(all_items),
        "papers": all_items,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(all_items)} items to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
