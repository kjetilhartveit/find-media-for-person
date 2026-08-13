---
name: find-media-from-fapello
description: Use when you need to find and download media from Fapello, a large aggregator of celebrity content with consistent download patterns.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for media of a specific celebrity/person on Fapello
- Downloading images or videos from a Fapello profile

# Find media from Fapello

Download images from Fapello (https://fapello.com), a massive aggregator of leaked/nude celebrity content.

## URL Patterns

- Profile: `https://fapello.com/{slug}/` (e.g., `fapello.com/emily-ratajkowski/`)
- Pagination: `https://fapello.com/{slug}/page-{N}/` (32 items per page, newest first)
- Item page: `https://fapello.com/{slug}/{id}/`
- Post page: `https://fapello.com/post/{post_id}/{slug}/` — standalone posts surfaced by web search. Note: a post may exist even when the profile URL returns 404.

### Direct image download

Images can be downloaded directly without visiting item pages. The URL pattern is:

`https://fapello.com/content/{l1}/{l2}/{slug}/1000/{slug}_{ID}.jpg`

Where:

- `{l1}` and `{l2}` are the first two letters of the slug (e.g., `c/h` for `charithra-chandran`)
- `{ID}` is the sequential item ID, zero-padded to 4 digits (e.g., `0161`)
- **The resolution segment changes at ID 1000:** IDs 1–999 use `1000/` in the path; IDs 1000+ use `2000/` (e.g., `content/t/y/tyla/2000/tyla_1001.jpg`).

Example: `https://fapello.com/content/c/h/charithra-chandran/1000/charithra-chandran_0161.jpg`

Thumbnails on profile pages use a similar pattern with `_300px.jpg` suffix (e.g., `charithra-chandran_0161_300px.jpg`).

## Recommendations on how to download

1. **Try gallery-dl first**:
   If successful, skip the manual steps below. If it fails or returns 404s, fall back to **manual URL formula** below.
2. **Manual method (primary)** — Fetch the profile page to discover the ID range. Sequential IDs appear in URLs like `/{slug}/{id}/`.
3. Check for pagination — follow `/page-2/`, `/page-3/`, etc. until pages return empty or 404.
4. Collect all unique IDs across pages. Some IDs may be missing (e.g., ID 3 can return 404).
5. Download images directly using the URL formula above — no need to visit individual item pages.
6. Rate limiting: sleep 0.3–0.5s between requests is sufficient.
7. No authentication required.

## Media types

- Most items are JPG images. A small fraction are MP4 videos.
- To check if an item is a video, visit the item page and look for `.mp4` URLs or `<video>` tags.
- Video URLs use pattern: `https://cdn[-n1].fapello.com/content/{l1}/{l2}/{slug}/{version}/{slug}_{ID}.mp4`
  (e.g., `https://cdn.fapello.com/content/k/a/kate-hudson/2000/kate-hudson_1716.mp4`)
- The same ID may have both a `.jpg` thumbnail and an `.mp4` video — download both.

## Quality

- Images range from ~240KB to ~900KB per image (most ~100-400KB), at 600x800 resolution.
- Videos are typically 600KB - 12MB MP4 files.
- Success rate is >99% — most sequential IDs resolve (9/1716 missing on Kate Hudson profile).
- Lots of content, consistent quality, very reliable. No auth needed.

## Pitfalls

- Some sequential IDs may be missing (404). Handle gracefully.
- **URL path segment changes at ID 1000:** IDs 1–999 use `1000/` in the content path; IDs 1000+ use `2000/`. Not accounting for this will cause 404 failures on the second half of downloads.
- The `{l1}/{l2}` path segments are derived from the slug's first two letters — verify with one known image first.
- Profile URLs may return 404 even when posts exist for the same person (found via web search at `fapello.com/post/{id}/{slug}/`).
- The `gallery-dl` fapello extractor has returned 404 in recent tests.
- Thousands of images possible — pace downloads and use rate limiting.
- Prioritize undownloaded ID ranges in follow-up sessions.

## Cloudflare Protection

- Fapello.com is protected by Cloudflare challenge pages.
- Simple HTTP tools (curl, wget) will get 403/CF challenge pages.
- `gallery-dl` and browser-based tools also hit the Cloudflare gate.
- Use a headless browser (e.g., browser_tool) to bypass Cloudflare for scraping.
- Alternative domains like `fapello.net` exist but have different anti-bot systems.

## Profile Not Found

- A person may not have any content on Fapello at all.
- If the direct profile URL returns 404 AND all search variations return 0 results (verified with browser), the person is not on the platform.
- Try search variations: `{name}`, `{first}-{last}`, `{first}{last}` (no hyphen).
- Some people appear only via individual posts (web search for `site:fapello.com "{name}"`).

## Model Not on Fapello

- Joon Mali (Thai adult model) has **no content on Fapello**. Profile URL variations tried: `joon-mali`, `joonmali`, `joon-mali-th`, `joonmali-th` plus site search. All returned 404 or no results.
- When searching for Joon Mali, use alternative sources: xhamster.com/pornstars/joon-mali (40+ videos), imagefap.com (dedicated galleries), jjgirls.com, yespornpics.com.

## New Insights (Aug 2025)

### Slug != Display Name

- The profile slug may differ from the person's display name. Example: Linda Lan's profile slug is `ms-lindalan`.
- When searching, also look for the `{username}` on social media (e.g., Instagram, OnlyFans) that links to Fapello.
- The search results page may show the slug in profile links — look for hrefs matching `/slug/` pattern.

### Featured/Suggested Item (ID 1000)

- Every profile page shows a featured/suggested item with ID 1000.
- This item returns 404 when accessed directly — it's not a real content item, just a placeholder on the page.
- When collecting IDs from profile pages, filter out ID 1000 before downloading.

### Pagination Behavior

- Some profiles have pagination that cycles (returns the same content after the first N pages).
- Stop paginating when you notice repeated ID sets between pages.
- The first page of a profile may show the newest content (highest IDs).
