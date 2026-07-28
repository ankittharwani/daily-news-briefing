#!/usr/bin/env python3
"""
Sets the "img" field of every story in a content.json from a verified
{article_url: image_url} map, matching on the story's "url".

Usage:
    python3 patch_images.py --data content.json --map images.json

Why this exists: hand-editing content.json is how image URLs get silently
dropped — a story keeps its text and link but loses its photo, and nothing
errors. Driving images from an explicit map, keyed on the article URL, makes
the omission visible: the script reports exactly which stories ended up
without an image and which map entries went unused.

images.json is {"https://article-url": "https://image-url" | null, ...}

Also normalises every image URL to https, because an http:// image embedded in
the https site is silently blocked by browsers as mixed content — one of the
easiest ways to ship invisible breakage.
"""

import argparse
import json


def normalise(url):
    if not url:
        return None
    url = url.strip()
    if url.startswith("http://"):
        url = "https://" + url[len("http://"):]
    if not url.startswith("https://"):
        return None
    return url


def walk_stories(data):
    """Yields every story dict in the content file, whatever section it's in."""
    for section in data.get("sections", []):
        for s in section.get("stories", []):
            yield s
    for group in data.get("country_groups", []):
        for s in group.get("stories", []):
            yield s
    for s in data.get("portfolio", []) or []:
        yield s
    for s in data.get("doha_events", []) or []:
        yield s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--map", required=True)
    args = ap.parse_args()

    with open(args.data) as f:
        data = json.load(f)
    with open(args.map) as f:
        raw_map = json.load(f)

    img_map = {k: normalise(v) for k, v in raw_map.items()}

    used, missing, applied = set(), [], 0
    for story in walk_stories(data):
        url = story.get("url")
        if url in img_map:
            used.add(url)
            story["img"] = img_map[url]
            if img_map[url]:
                applied += 1
            else:
                missing.append(story["headline"][:70])
        else:
            if not story.get("img"):
                missing.append(story["headline"][:70])

    with open(args.data, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    total = sum(1 for _ in walk_stories(data))
    print(f"{applied}/{total} stories have a verified image.")
    if missing:
        print(f"\n{len(missing)} without an image (fallback icon will render):")
        for m in missing:
            print(f"  - {m}")
    unused = set(img_map) - used
    if unused:
        print(f"\n{len(unused)} map entries matched no story (check for URL drift):")
        for u in unused:
            print(f"  - {u}")


if __name__ == "__main__":
    main()
