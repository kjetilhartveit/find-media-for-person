---
name: find-media-from-pictoa
description: Download high-quality media from Pictoa by scraping album pages for image URLs.
---

# Find media from Pictoa

Download images from Pictoa (https://www.pictoa.com), a gallery site with albums of celebrity content.

## URL Patterns

- Site: `https://www.pictoa.com`
- Search URL: `https://www.pictoa.com/s/<query>/` (e.g. `https://www.pictoa.com/s/jessi/`). Queries with spaces use `+` (e.g. `/s/jessi+kpop/`). Unicode queries URL-encoded (e.g. `/s/%EC%A0%9C%EC%8B%9C/` for "제시").
- Search form (alternative): POST to `https://www.pictoa.com/search-by-form` with body `_token=<csrf>&q=<query>`. The CSRF token is found in `<meta name="csrf-token" content="...">` on the homepage. This returns a redirect to `/s/<query>/`.
- Old URL formats like `/search/<query>.html` or `/search?query=<query>` return 404 — do not use.
- Album URL pattern: `https://www.pictoa.com/albums/<title>-<id>.html`
- Image CDN: `t1.pictoa.com` — serves actual images (~15-35KB JPEG). Use these URLs as-is.
- NOTE: `s2.pictoa.com` previously served high-quality versions by swapping `t1` → `s2` in URLs. As of 2026-07-18 this CDN returns 404. Only `t1.pictoa.com` works.
- Example image URL: https://t1.pictoa.com/media/galleries/164/015/164015593e5b1db71d5/2919079593e5b1dba2c5.jpg

## Recommendations on how to download

1. Search using the `/s/<query>/` URL pattern. Try multiple query variations (celebrity name, handle, real full name, performer name, foreign names - like Korean and Chinese - if applicable).
2. Parse search results for album links matching `https://www.pictoa.com/albums/...html`. Filter for relevance — generic name searches may return unrelated adult performers with similar names.
3. Fetch each album page to extract image URLs from `src` attributes pointing to `t1.pictoa.com`.
4. Extract actual album images (not related gallery thumbnails) by filtering for URLs containing the album ID.
5. Rate limiting: sleep 0.3–0.5s between requests.
6. Use a user-agent header like `"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"`.

## Quality

- Images range from ~15KB to ~35KB per file from the `t1` CDN.
- Decent quality for thumbnails/gallery previews.

## Pitfalls

- **Search requires `/s/<query>/` URL format.** Old patterns (`/search/<q>.html`, `/search?query=<q>`) return 404.
- **No direct celebrity URLs.** You must search and filter results manually.
- **Relevance filtering is important.** A simple name search (e.g. "jessi") may return unrelated performers sharing the same name. Try adding disambiguating terms (handle, full name, performer name).
- **The `s2` CDN is broken.** The former advice to swap `//t1.` → `//s2.` for higher quality no longer works and returns 404 — use `t1` URLs as-is.
- Labor-intensive: one page fetch per album to extract all image URLs.
- **No "No Results" indicator on empty search.** A search returning no albums shows `No Results` in the page body but still returns a 200 status code — check the HTML for `<p id="noResults">`.
