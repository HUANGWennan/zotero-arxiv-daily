#!/usr/bin/env python3
"""Public RSS metadata snapshot for a cloud journal watch. Python stdlib only."""
import datetime as dt
import email.utils
import html
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent
OUTPUT = ROOT / "public" / "latest.json"
FEEDS = {
    "Cambridge Journal of Economics": "https://academic.oup.com/rss/site_5437/3298.xml",
    "Contributions to Political Economy": "https://academic.oup.com/rss/site_5445/3306.xml",
    "Economic Systems Research": "https://www.tandfonline.com/feed/rss/cesr20",
    "International Journal of Political Economy": "https://www.tandfonline.com/feed/rss/mijp20",
    "International Review of Applied Economics": "https://www.tandfonline.com/feed/rss/cira20",
    "New Political Economy": "https://www.tandfonline.com/feed/rss/cnpe20",
    "Review of Political Economy": "https://www.tandfonline.com/feed/rss/crpe20",
    "Structural Change and Economic Dynamics": "https://rss.sciencedirect.com/publication/science/0954349X",
}
USER_AGENT = "JournalRSSWatch/1.0 (public journal metadata; weekly research monitoring)"
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s<>\"']+", re.I)

def local(tag):
    return tag.rsplit("}", 1)[-1].split(":")[-1].lower()

def contents(node):
    return html.unescape(" ".join("".join(node.itertext()).split()))

def field(node, names):
    for name in names:
        for child in node:
            if local(child.tag) == name.lower():
                if name == "link" and child.get("href"):
                    return child.get("href", "").strip()
                return contents(child)
    return ""

def normalize_date(value):
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = email.utils.parsedate_to_datetime(value)
        except (TypeError, ValueError, IndexError):
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")

def pull(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*"}
    )
    with urllib.request.urlopen(request, timeout=35) as response:
        size = 0
        chunks = []
        while True:
            chunk = response.read(131072)
            if not chunk:
                break
            size += len(chunk)
            if size > 12_000_000:
                raise ValueError("feed larger than 12 MB")
            chunks.append(chunk)
        return b"".join(chunks), response.status, response.headers.get("Content-Type", "")

def parse_feed(raw):
    root = ET.fromstring(raw)
    items = [node for node in root.iter() if local(node.tag) in ("item", "entry")]
    if not items:
        raise ValueError("XML parsed but no RSS/Atom items were present")
    parsed = []
    for item in items:
        title = field(item, ["title"])
        if not title:
            continue
        link = field(item, ["link"])
        date_raw = field(item, ["pubdate", "date", "published", "updated", "issued", "created"])
        date = normalize_date(date_raw)
        identifier = field(item, ["identifier", "guid", "id"])
        summary = field(item, ["description", "summary", "abstract"])
        doi_candidate = DOI_RE.search(" ".join([identifier, link, summary[:1500]]))
        doi = doi_candidate.group(0).rstrip(".,);]") if doi_candidate else None
        parsed.append({
            "title": title, "link": link, "identifier": identifier,
            "doi": doi, "feed_date": date, "raw_date": date_raw,
            "summary_excerpt": summary[:550]
        })
    unique = {}
    for item in parsed:
        key = (item["doi"] or item["link"] or item["title"]).lower()
        if key not in unique or (item["feed_date"] or "") > (unique[key]["feed_date"] or ""):
            unique[key] = item
    return sorted(unique.values(), key=lambda x: x["feed_date"] or "", reverse=True)

def main():
    now = dt.datetime.now(dt.timezone.utc)
    old = {}
    if OUTPUT.exists():
        try:
            previous = json.loads(OUTPUT.read_text(encoding="utf-8"))
            old = {f["journal"]: f for f in previous.get("feeds", [])}
        except (OSError, ValueError, KeyError):
            pass
    feeds = []
    for journal, url in FEEDS.items():
        record = {"journal": journal, "rss_url": url, "checked_utc": now.isoformat(), "status": "error"}
        try:
            raw, status, ctype = pull(url)
            items = parse_feed(raw)
            latest_date = items[0]["feed_date"]
            latest_dt = dt.datetime.fromisoformat(latest_date.replace("Z", "+00:00")) if latest_date else None
            record.update({
                "status": "ok", "http_status": status, "content_type": ctype,
                "items_count": len(items), "latest_feed_date": latest_date,
                "possibly_stale": latest_dt is None or (now - latest_dt).days > 14,
                "items": items,
            })
        except Exception as exc:
            record["error"] = "%s: %s" % (type(exc).__name__, str(exc)[:260])
            prior = old.get(journal, {})
            if prior.get("items"):
                record.update({"status": "cached_after_error",
                               "items": prior["items"], "items_count": len(prior["items"]),
                               "latest_feed_date": prior.get("latest_feed_date"),
                               "cache_last_checked_utc": prior.get("checked_utc")})
        feeds.append(record)
        print(journal + ": " + record["status"] + ", " + str(record.get("items_count", 0)) + " items", flush=True)
        time.sleep(0.4)
    good = sum(1 for x in feeds if x["status"] == "ok")
    snapshot = {
        "schema_version": 1, "generated_utc": now.isoformat(),
        "status": "ok" if good == len(FEEDS) else ("partial" if good else "error"),
        "ok_feeds": good, "total_feeds": len(FEEDS),
        "note": "Feed dates can lag first-online publication. Always cross-check publisher pages and DOIs.",
        "feeds": feeds,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Small companion snapshot avoids loading all historical RSS entries into an LLM.
    cutoff = (now - dt.timedelta(days=90)).isoformat()
    compact_feeds = []
    for feed in feeds:
        recent = []
        for item in feed.get("items", []):
            if item["feed_date"] is None or item["feed_date"] >= cutoff:
                recent.append({k: item.get(k) for k in ("title", "link", "doi", "feed_date")})
        compact_feeds.append({
            "journal": feed["journal"], "status": feed["status"],
            "checked_utc": feed["checked_utc"], "latest_feed_date": feed.get("latest_feed_date"),
            "possibly_stale": feed.get("possibly_stale", True),
            "total_feed_items": feed.get("items_count", 0),
            "items": recent[:40], "filtered_or_capped": len(recent) > 40,
            "error": feed.get("error")
        })
    compact = {
        "schema_version": 1, "generated_utc": snapshot["generated_utc"],
        "status": snapshot["status"], "ok_feeds": good, "total_feeds": len(FEEDS),
        "note": snapshot["note"], "feeds": compact_feeds,
    }
    compact_path = OUTPUT.parent / "latest_compact.json"
    compact_path.write_text(json.dumps(compact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("RESULT:", snapshot["status"], good, "/", len(FEEDS))
    return 0 if good else 2

if __name__ == "__main__":
    sys.exit(main())
