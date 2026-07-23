---
name: find-media-from-fapello
description: Download media from Fapello, a large aggregator of celebrity content with consistent download patterns.
---

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

1. Fetch the profile page to discover the ID range. Sequential IDs appear in URLs like `/{slug}/{id}/`.
2. Check for pagination — follow `/page-2/`, `/page-3/`, etc. until pages return empty or 404.
3. Collect all unique IDs across pages. Some IDs may be missing (e.g., ID 3 can return 404).
4. Download images directly using the URL formula above — no need to visit individual item pages.
5. Rate limiting: sleep 0.3–0.5s between requests is sufficient.
6. No authentication required.

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
