---
name: find-media-from-fappeningbook
description: Download media from Fappeningbook, a large aggregator with full-size images available from thumbnails.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# Find media from Fappeningbook

Download images from Fappeningbook (https://fappeningbook.com), a large aggregator with galleries.

## URL Patterns

- Profile: `https://fappeningbook.com/{slug}-nude/` — try the person's name first (e.g. `caroline-nitter-nude/`), then their Instagram username if that 404s (e.g. `jessicah-o-nude/` for @jessicah_o). The `us.fappeningbook.com` subdomain also exists but mirrors the same content.
- Image URLs: `https://fappeningbook.com/photos/{l1}/{l2}/{slug}/1000/{id}t.jpg` (thumbnail) → remove `t` for full-size (e.g. `1t.jpg` → `1.jpg`). The resolution segment is consistently `1000`.

## Recommendations on how to download

- Extract thumbnail URLs from the page HTML using a **specific** pattern that matches only actual photos: look for URLs matching `/photos/.../{id}t.jpg`. A broad grep for `*.jpg` will also pick up avatars (`/avatars/.../avatar.jpg`), site assets (`/assets/*`), and related-profile thumbnails — these should be excluded.
- IDs are sequential per page (e.g. 1–26). Thumbnails appear in reverse order in the HTML (highest ID first). Check for pagination links; smaller profiles may have all images on a single page.
- Rate limiting: sleep 0.3–0.5s between requests.
- Download all thumbnails' full-size counterparts — don't skip any based on position. Validate by checking file size > 10KB after download.

## Quality

- Images range from ~42KB to ~922KB. Generally good quality for an aggregator site. No video content on most profiles.

## Pitfalls

- Site search (`/?s=query`) returns 200 but might not yield any useful results — prefer direct profile URLs instead.
- Some profiles may not exist under a person's real name; try their social media handle as fallback.
- Some thumbnails may not resolve to valid full-size images even after removing the `t` suffix — check response code and file size.
- No high-thumb (`h` or `ht`) variant exists — only the `t` (thumbnail) and full-size versions are available.
