#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Scan Israeli media for an entity via Google News RSS (no key).

  media_scan.py "חברה לדוגמה" --alias "Example Ltd" [--sites] [--extra "word1" "word2"]

Runs each exact name on its own, then (--sites) per main Israeli outlet, then optional
name+extra-word queries. Dedupes, sorts newest first, prints JSON. Headlines only: a hit
means Google matched the article, NOT that the headline is about the entity. Read it.
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

SITES = ["globes.co.il", "themarker.com", "calcalist.co.il", "bizportal.co.il", "ynet.co.il",
         "haaretz.co.il", "mako.co.il", "maariv.co.il", "israelhayom.co.il", "walla.co.il",
         "nadlancenter.co.il", "ice.co.il", "timesofisrael.com", "jpost.com"]


def rss(q, lang):
    p = {"he": {"hl": "he", "gl": "IL", "ceid": "IL:he"},
         "en": {"hl": "en-IL", "gl": "IL", "ceid": "IL:en"}}[lang]
    u = "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": q, **p})
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return ET.fromstring(r.read()).findall(".//item")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name")
    ap.add_argument("--alias", nargs="*", default=[])
    ap.add_argument("--extra", nargs="*", default=[])
    ap.add_argument("--sites", action="store_true")
    ap.add_argument("--delay", type=float, default=1.0)
    a = ap.parse_args()

    names = [a.name, *a.alias]
    queries = [f'"{n}"' for n in names]
    if a.sites:
        queries += [f'"{n}" site:{s}' for n in names for s in SITES]
    queries += [f'"{n}" {x}' for n in names for x in a.extra]

    hits, log = {}, []
    for q in queries:
        lang = "he" if any("֐" <= c <= "׿" for c in q) else "en"
        try:
            items = rss(q, lang)
        except (urllib.error.URLError, ET.ParseError, TimeoutError) as e:
            log.append({"query": q, "error": str(e)[:120]})
            continue
        log.append({"query": q, "results": len(items)})
        for i in items:
            title = (i.findtext("title") or "").strip()
            src = (i.findtext("source") or "").strip()
            try:
                date = parsedate_to_datetime(i.findtext("pubDate")).date().isoformat()
            except (TypeError, ValueError):
                date = None
            h = hits.setdefault((title, date), {"date": date, "source": src, "title": title,
                                                "url": i.findtext("link"), "queries": []})
            h["queries"].append(q)
            h["name_in_headline"] = any(n in title for n in names)
        time.sleep(a.delay)

    out = sorted(hits.values(), key=lambda h: h["date"] or "", reverse=True)
    print(json.dumps({"names": names, "unique_articles": len(out), "queries": log, "articles": out},
                     ensure_ascii=False, indent=1))
    return 1 if log and all("error" in x for x in log) else 0


if __name__ == "__main__":
    sys.exit(main())
