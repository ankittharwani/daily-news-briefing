#!/usr/bin/env python3
"""
Adds (or replaces) one day's entry in the archive's manifest.json.

Usage:
    python3 update_manifest.py --manifest site/manifest.json \
        --date 2026-07-29 --weekday Wednesday \
        --display-date "Wednesday, July 29, 2026" \
        --month-label "July 2026" \
        --file "briefings/2026-07-29.html" \
        --caption "One-line most notable story of the day."

If --manifest does not exist yet, it is created with a single entry.
If an entry for --date already exists, it is replaced (idempotent re-runs
for the same day, e.g. if you need to regenerate today's edition, are safe).
"""
import argparse
import json
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--weekday", required=True)
    ap.add_argument("--display-date", required=True)
    ap.add_argument("--month-label", required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--caption", required=True)
    ap.add_argument("--hero-image", default=None,
                    help="Real photo URL from the day's lead story; drives the home page "
                         "hero and edition cards. Omit if none was verified — a dated "
                         "fallback tile renders instead. Never invent a URL.")
    args = ap.parse_args()

    if os.path.exists(args.manifest):
        with open(args.manifest) as f:
            data = json.load(f)
    else:
        data = []

    data = [d for d in data if d.get("date") != args.date]
    entry = {
        "date": args.date,
        "weekday": args.weekday,
        "display_date": args.display_date,
        "month_label": args.month_label,
        "file": args.file,
        "caption": args.caption,
    }
    if args.hero_image:
        entry["hero_image"] = args.hero_image
    data.append(entry)
    # newest first
    data.sort(key=lambda d: d["date"], reverse=True)

    os.makedirs(os.path.dirname(args.manifest) or ".", exist_ok=True)
    with open(args.manifest, "w") as f:
        json.dump(data, f, indent=2)
    print(f"manifest now has {len(data)} entries; wrote {args.manifest}")


if __name__ == "__main__":
    main()
