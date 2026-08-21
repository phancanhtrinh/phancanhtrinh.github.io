---
layout: post
title: "Email Archive Manager: turn scattered mail into a private, searchable archive"
meta_title: "Email Archive Manager tutorial | TrinhPHAN"
description: "Build a private local archive across Gmail, Outlook, PST, and EML; deduplicate messages, organize attachments, search decisions, create reports, and verify integrity."
summary: "A practical guide to consolidating Gmail, Outlook, PST, and EML into a private local archive with exact deduplication, traceable attachments, full-text search, reports, and integrity checks."
author: Phan-Canh Trinh
categories:
  - eng_tut
permalink: /tutorials/email-archive-manager/
---

<p class="tutorial-lede">Managing several email addresses with years of conversations is tricky. We need a better way to capture important information, connect related messages, and summarize decisions when we need them later.</p>

Work rarely stays inside one inbox. A project may begin in Gmail, continue in an institutional Outlook account, and leave behind old PST or EML exports after a job or computer change. The same mail can appear in several sources. Attachments become detached from their context, while the decision you remember remains buried somewhere in a long thread.

**Email Archive Manager** is a portable Codex skill for turning those sources into a private, local, searchable archive. It keeps messages and attachments on your computer, preserves where every item came from, and gives Codex a consistent workflow for retrieval, summaries, reports, verification, and migration.

<nav class="tutorial-toc" aria-label="Table of contents">
<strong>In this tutorial</strong>
<ol>
<li><a href="#what-it-builds">What it builds</a></li>
<li><a href="#install-the-skill">Install the skill</a></li>
<li><a href="#inventory-and-authorize">Inventory and authorize sources</a></li>
<li><a href="#ingest-and-reconcile">Ingest and reconcile mail</a></li>
<li><a href="#attachments">Organize attachments</a></li>
<li><a href="#search-summarize-report">Search, summarize, and report</a></li>
<li><a href="#worked-example">Worked research example</a></li>
<li><a href="#verify-and-migrate">Verify and migrate</a></li>
<li><a href="#privacy-and-security">Privacy and security</a></li>
<li><a href="#weekly-updates">Optional weekly updates</a></li>
</ol>
</nav>

## What it builds {#what-it-builds}

The workflow separates original sources, canonical messages, and stored files so each layer can be checked independently.

<div class="archive-flow" aria-label="Archive workflow">
  <div class="archive-step"><span>1 · Collect</span><strong>Mail sources</strong>Gmail, Outlook, PST, and EML are inventoried without changing the originals.</div>
  <div class="archive-step"><span>2 · Reconcile</span><strong>Searchable records</strong>Exact duplicates share a canonical message while every source occurrence remains traceable.</div>
  <div class="archive-step"><span>3 · Retrieve</span><strong>Answers and files</strong>Search results, summaries, HTML reports, and readable attachment links stay local.</div>
</div>

The archive uses SQLite for message metadata and full-text search. Each message retains its account, folder, source type, source record ID, import run, and—when available—raw-message hash. This provenance matters: finding a message is useful; knowing whether it came from an old export, a current mailbox, or both makes the result defensible.

## Install the skill {#install-the-skill}

Download the portable package, unzip it, and place the entire `email-archive-manager` folder in your personal Codex skills directory:

- **macOS and Linux:** `~/.codex/skills/email-archive-manager`
- **Windows:** `%USERPROFILE%\.codex\skills\email-archive-manager`

Restart Codex if it is already running. Keep automatic skill selection enabled, or invoke the workflow explicitly by saying `$email-archive-manager` in your request.

<div class="download-panel">
  <p><strong>Portable skill package</strong><br>Generic instructions, source guides, archive contract, and the standard-library Python helper.</p>
  <a class="download-button" href="/downloads/email-archive-manager.zip" download>Download ZIP</a>
</div>

The helper requires Python 3 and uses only the standard library. Run commands from inside the installed skill folder. For example:

```bash
python3 scripts/email_archive.py init --root "/Users/you/EmailArchive"
```

On Windows, use `py` if that is how Python is installed:

```powershell
py scripts\email_archive.py init --root "D:\EmailArchive"
```

## Inventory and authorize sources {#inventory-and-authorize}

Before importing anything, ask Codex to inventory the sources you want to retain. A good request is:

> Use `$email-archive-manager` to inventory my mail sources. Do not access or import an account until I approve that account and the archive destination.

For each source, record the account, source type, path or API identity, approximate size, date range, attachment policy, and a stable fingerprint. Decide whether Deleted, Junk, and Drafts belong in scope. Also identify overlaps: an institutional Outlook mailbox may already contain messages found in a PST backup or EML export.

Authorization is source-specific and read-only. Approving access to one mailbox does not approve another, and it never grants permission to send, delete, move, label, reply to, or mark messages as read.

## Ingest and reconcile mail {#ingest-and-reconcile}

Start the local archive once:

```bash
python3 scripts/email_archive.py init --root "/path/to/EmailArchive"
```

Then use the adapter that fits each source:

| Source | Recommended path | Important detail |
|---|---|---|
| EML folder | Bundled `import-eml` helper | Recursively imports messages, readable bodies, source paths, and attachments. |
| PST | Hash the immutable PST, then export with a trusted PST parser | For damaged or legacy PSTs, compare two parsers when practical and retain warnings. |
| Outlook for Windows | Explicit PST/EML export or read-only Outlook automation | OST is only a cache and may be incomplete or encrypted. |
| Outlook for Mac | Read-only database inventory plus a SQLite backup snapshot | Include WAL data through the SQLite backup API; never copy only the main live database. |
| Gmail / Google Workspace | Read-only Gmail connector/API, then Takeout as fallback | Preserve Gmail message/thread IDs and labels; do not store OAuth or browser credentials. |

Import an EML tree with an account label that identifies its provenance:

```bash
python3 scripts/email_archive.py import-eml \
  --root "/path/to/EmailArchive" \
  --account "research-account" \
  --source-name "2026-transition-export" \
  "/path/to/eml-export"
```

Deduplication is deliberately conservative:

- **Exact duplicates** can be linked using a normalized Message-ID, raw-message hash, or deterministic content hash.
- **Probable duplicates** may share a unique normalized subject, exact timestamp, and compatible participants, but are labeled as probable rather than silently merged.
- **Related messages**—for example, a reply quoting an older note—remain separate records.

When current mail overlaps an old PST or EML export, reconcile the sources into the same archive. One canonical message may have several source records, so removing duplicate display rows never removes provenance.

## Attachments that remain usable {#attachments}

Attachments are stored by the SHA-256 digest of their exact bytes. A blob lives at a path such as `attachments/blobs/7a/7a…`, and identical bytes are stored only once even if they were attached to several messages.

Content-addressed storage is excellent for integrity but awkward for people, so the archive also creates a readable view by account, year, date, and message. Original filenames are sanitized for the filesystem but retained in metadata. Type detection starts with the file signature, then considers the filename and MIME type; the index can therefore say which software normally opens a file.

<div class="attachment-grid">
  <div class="attachment-card"><strong>03_Project-kickoff.pptx</strong><small>Microsoft PowerPoint presentation<br>Opens with Microsoft PowerPoint</small></div>
  <div class="attachment-card"><strong>02_Sample-plan.xlsx</strong><small>Microsoft Excel workbook<br>Opens with Microsoft Excel</small></div>
  <div class="attachment-card"><strong>01_Methods-review.pdf</strong><small>PDF document<br>Opens with Preview or Adobe Acrobat</small></div>
</div>

Every readable file links back to its stored blob and message relationship. Inline signature graphics are retained as relationships but can be distinguished from substantive documents.

## Search, summarize, and report {#search-summarize-report}

The helper provides direct full-text search:

```bash
python3 scripts/email_archive.py search \
  --root "/path/to/EmailArchive" \
  '"sample shipment" AND timeline'
```

Codex can then turn retrieved evidence into a timeline, decision log, action-item list, or attachment inventory. Ask for source citations in the answer so each conclusion can be traced to a message and archive path.

Create a local, searchable HTML overview with:

```bash
python3 scripts/email_archive.py report --root "/path/to/EmailArchive"
```

The report summarizes coverage by account, recent messages, and attachment counts. Project-specific reports can add deduplicated thread counts, timelines, action items, and clickable local attachment paths. Email content must be HTML-escaped before embedding.

## Worked example: an anonymized research collaboration {#worked-example}

<div class="example-panel">
<strong>Fictional scenario</strong>

Dr. Rivera is coordinating the invented **Northstar Tissue Atlas** study. Messages are split among a personal Gmail account, a university Outlook mailbox, and a 2024 PST export. The same kickoff thread appears in Outlook and the PST; later shipping notes exist only in Gmail. No real people, institutions, addresses, or files are used in this example.

<div class="example-question"><strong>Natural-language question</strong><br>“What did the Northstar team decide about the pilot samples, who owns each next step, and which files support those decisions?”</div>

After exact duplicate reconciliation, Codex searches the canonical messages and returns:

| Date | Timeline and decision | Action item | Evidence |
|---|---|---|---|
| 4 Mar 2026 | Team selected a 12-sample pilot before expanding the cohort. | Rivera: circulate the finalized sample table by 6 Mar. | Kickoff thread; `Project-kickoff.pptx` |
| 6 Mar 2026 | Sample IDs and three processing batches were confirmed. | Chen: verify batch labels before shipment. | Planning reply; `Sample-plan.xlsx` |
| 10 Mar 2026 | Shipment moved to 14 Mar to accommodate cold-chain pickup. | Morgan: send the courier confirmation. | Logistics thread; `Methods-review.pdf` |

The answer notes that the kickoff mail occurred in two sources but counts it once. Its provenance still lists both `outlook/current-mailbox` and `pst/2024-export`. The attachment section links readable filenames such as `03_Project-kickoff.pptx`, `02_Sample-plan.xlsx`, and `01_Methods-review.pdf`, while the underlying SHA-256 blobs provide integrity and exact-file deduplication.
</div>

## Verify, migrate, and recover with confidence {#verify-and-migrate}

Run verification after every major import and before claiming the archive is complete:

```bash
python3 scripts/email_archive.py verify --root "/path/to/EmailArchive"
```

Verification checks SQLite integrity and foreign keys, confirms the search-index count matches the canonical message count, and verifies that every registered attachment exists with the stored size and SHA-256. It also flags messages that claim attachments but have no saved attachment rows. Import reports should state gaps such as missing bodies, inaccessible cloud links, parser warnings, unsupported OST files, or preview-only messages.

To migrate, copy both the archive root and the skill folder to the new computer—never mailbox credentials. If the archive is in a synchronized folder, wait until every file is available locally. Run `verify` before connecting a new account, add that account as a new provenance origin, and reconcile exact duplicates with the existing records.

## Privacy and security boundaries {#privacy-and-security}

<div class="security-panel">
<strong>The archive is private by design, but its location and reports still matter.</strong>

- Never store passwords, OAuth tokens, OTPs, session cookies, access keys, or other credentials in the archive.
- The workflow is read-only: it does not authorize sending, deleting, moving, labeling, replying to, or marking email as read.
- Keep directories private (`0700`) and database/attachment files private (`0600`) where the operating system supports POSIX permissions.
- Think carefully before choosing OneDrive, Dropbox, iCloud Drive, or another cloud-synchronized root. Synchronization changes who or what may receive copies.
- Never put private signed URLs in HTML reports. Record a portal home page and a shared-folder name instead, with access requirements noted separately.
- Do not publish archive reports. They may contain message text, participant details, filenames, and local paths even when credentials are excluded.
</div>

## Optional weekly updates {#weekly-updates}

Once the initial archive verifies successfully, you can ask Codex to create a weekly update—but only after separately authorizing the recurring job and each source. A practical incremental import uses an eight-day overlap to catch delayed synchronization, then upserts by source record ID and reconciles exact identities.

Each run should save a dated digest with imported, duplicate, recovered, and failed counts; parser or access warnings; attachment status; and the final verification result. If authentication expires, the job should stop and ask you to reconnect. It must never extract or reuse browser cookies or session credentials.

The result is not just another mailbox backup. It is a durable local knowledge base: searchable across accounts, careful about duplicates, explicit about provenance, useful for summarizing decisions, and verifiable before you trust or move it.
