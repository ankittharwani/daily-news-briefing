#!/usr/bin/env python3
"""
Builds search-index.json by walking every rendered briefing in briefings/.

Usage:
    python3 build_search_index.py --briefings-dir site/briefings --out site/search-index.json

This is what turns the archive from "a list of dates" into something you can
actually interrogate — "what have I read about Iran?" — across every edition.
Run it after rendering each new day's briefing, before committing.

It parses the HTML this same repo generated (rather than the source content JSON)
so that older editions, whose content JSON is long gone from any local disk, are
still fully indexed.
"""

import argparse
import glob
import html
import json
import os
import re

SECTION_LABELS = {
    "sports": "Sports",
    "business": "Business & Markets",
    "ai": "AI & Technology",
    "geopolitics": "Geopolitics",
    "portfolio": "Market Watch",
    "country": "Country Updates",
    "doha": "Doha Events",
}

SECTION_RE = re.compile(
    r'<section class="news-section"[^>]*data-section="([^"]+)"(.*?)</section>', re.S
)
CARD_RE = re.compile(
    r'<h3 class="headline">(.*?)</h3>\s*'
    r'<p class="story-text">(.*?)</p>\s*'
    r'<a class="read-more" href="([^"]*)"',
    re.S,
)
SKIM_RE = re.compile(r'<ol class="skim-list">(.*?)</ol>', re.S)
SKIM_ITEM_RE = re.compile(r'<span>(.*?)</span>\s*</li>', re.S)
TAG_RE = re.compile(r"<[^>]+>")


def clean(text):
    return html.unescape(TAG_RE.sub("", text)).strip()


def parse_file(path):
    date = os.path.splitext(os.path.basename(path))[0]
    with open(path, encoding="utf-8") as f:
        raw = f.read()

    records = []
    for key, block in SECTION_RE.findall(raw):
        label = SECTION_LABELS.get(key, key.title())
        for headline, body, url in CARD_RE.findall(block):
            records.append({
                "date": date,
                "section": label,
                "section_key": key,
                "headline": clean(headline),
                "body": clean(body),
                "url": url,
            })

    skim_match = SKIM_RE.search(raw)
    if skim_match:
        for item in SKIM_ITEM_RE.findall(skim_match.group(1)):
            records.append({
                "date": date,
                "section": "The Skim",
                "section_key": "skim",
                "headline": clean(item),
                "body": "",
                "url": "",
            })
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--briefings-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    all_records = []
    files = sorted(glob.glob(os.path.join(args.briefings_dir, "*.html")), reverse=True)
    for path in files:
        all_records.extend(parse_file(path))

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(all_records, f, ensure_ascii=False, separators=(",", ":"))

    print(f"Indexed {len(all_records)} entries from {len(files)} editions -> {args.out}")


if __name__ == "__main__":
    main()
