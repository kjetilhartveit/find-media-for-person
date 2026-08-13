---
name: find-media-from-pictoa
description: Use when you need to find and download high-quality media from Pictoa via gallery-dl (primary) with manual album parsing as fallback.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for albums of a specific person on Pictoa
- Searching Pictoa by query to find albums matching a person
- Scraping gallery pages from Pictoa

# Find media from Pictoa

Download images from Pictoa (https://www.pictoa.com), a gallery site with albums of celebrity content.

gallery-dl has `PictoaAlbumExtractor` and `PictoaImageExtractor` — use as **primary** method. Fall back to manual album page parsing below.

## Primary download method — Download via gallery-dl

`gallery-dl` supports Pictoa albums natively.

## Fallback download method — Manual album page parsing

When `gallery-dl` is unavailable or fails:

1. Search using the `/s/<query>/` URL pattern. Try multiple query variations (celebrity name, handle, real full name, performer name, foreign names - like Korean and Chinese - if applicable).
2. Also try category URLs like `/c/<celebrity-name>-<category-id>/`.
3. Parse search results for album links matching `https://www.pictoa.com/albums/...html`. Filter for relevance — generic name searches may return unrelated adult performers with similar names (e.g., "Anissa Kate" mixed in with "Kate Hudson").
4. Fetch each album page to extract image URLs from `data-lazy-src` attributes pointing to `t1.pictoa.com`.
5. Extract actual album images (not related gallery thumbnails) by filtering for URLs containing the album ID.
6. For pagination, check album page URLs for `-p2.html`, `-p3.html` patterns and include those.
7. Rate limiting: sleep 0.3–0.5s between requests.
8. Use a user-agent header like `"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"`.

### URL Patterns

- Site: `https://www.pictoa.com`
- Search URL: `https://www.pictoa.com/s/<query>/` (e.g. `https://www.pictoa.com/s/jessi/`). Queries with spaces use `+` (e.g. `/s/jessi+kpop/`). Unicode queries URL-encoded (e.g. `/s/%EC%A0%9C%EC%8B%9C/` for "제시").
- Search form (alternative): POST to `https://www.pictoa.com/search-by-form` with body `_token=<csrf>&q=<query>`. The CSRF token is found in `<meta name="csrf-token" content="...">` on the homepage. This returns a redirect to `/s/<query>/`.
- Old URL formats like `/search/<query>.html` or `/search?query=<query>` return 404 — do not use.
- Album URL pattern: `https://www.pictoa.com/albums/<title>-<id>.html`
- Album URL pattern (with internal image ID): `https://www.pictoa.com/albums/<title>-<id>.html/<img-id>.html` — both forms appear in search results and point to the same album.
- Album pagination: `https://www.pictoa.com/albums/<title>-<id>-p2.html`, `https://www.pictoa.com/albums/<title>-<id>-p3.html`, etc.
- Category URL pattern: `https://www.pictoa.com/c/<name>-<category-id>/` — category pages list multiple albums.
- Search pagination: `https://www.pictoa.com/s/<query>/p2/` — NOTE: p2 pagination was observed NOT to work (returns 404). Only use first page of search results.
- Image CDN: `t1.pictoa.com` — serves actual images (~15-35KB JPEG, up to ~48KB). Use these URLs as-is.
- NOTE: `s2.pictoa.com` previously served high-quality versions by swapping `t1` → `s2` in URLs. As of 2026-07-18 this CDN returns 404. Only `t1.pictoa.com` works.
- Example image URL: https://t1.pictoa.com/media/galleries/164/015/164015593e5b1db71d5/2919079593e5b1dba2c5.jpg

## Quality

- Images range from ~15KB to ~35KB per file from the `t1` CDN.
- Decent quality for thumbnails/gallery previews.

## Pitfalls

- **Search requires `/s/<query>/` URL format.** Old patterns (`/search/<q>.html`, `/search?query=<q>`) return 404.
- **No direct celebrity URLs.** You must search and filter results manually.
- **Relevance filtering is important.** A simple name search (e.g. "jessi") may return unrelated performers sharing the same name. Try adding disambiguating terms (handle, full name, performer name). Searching "sofie" alone returns 100+ albums of adult performers — not the celebrity you want.
- **POST to search-by-form redirects but -L fails.** The CSRF POST to `/search-by-form` returns a 302 redirect, but following it with `-L` may return 405. Get cookies, POST to populate session, then GET the search URL directly with those cookies.
- **The `s2` CDN is broken.** The former advice to swap `//t1.` → `//s2.` for higher quality no longer works and returns 404 — use `t1` URLs as-is.
- Labor-intensive: one page fetch per album to extract all image URLs.
- **No "No Results" indicator on empty search.** A search returning no albums shows `No Results` in the page body but still returns a 200 status code — check the HTML for `<p id="noResults">` or search returns 404.
- **Search returns 404 for non-existent queries.** If the search query has no results, the search URL may return 404 (not just 200 with No Results text).
- **Gallery ID regex challenge.** Album names contain dashes, so `[^-]+` pattern won't work. Use regex like `albums/.*?-(\d{7})` to extract the 7-digit gallery ID, or `albums/.*?-(\d{7})/\d+\.html` for nested paths.
- **Two album URL formats.** Some album links have a trailing `/image-id.html` (e.g., `/albums/kate-hudson-booty-3228997/75141781.html`). Extract the first 7-digit number after `-` as the gallery ID.
- **Image filtering by gallery ID.** The gallery ID (7 digits before `.html`) must be in the image URL path on the album page to filter out related gallery thumbnails. Album pages include `data-lazy-src` images from related/recommended galleries — only keep URLs containing the target gallery ID.
- **gallery-dl does not support pagination URLs.** Passing `-p2.html`, `-p3.html` etc. to gallery-dl returns "Unsupported URL". The extractor only handles the main album URL (`-p1.html` implicitly). To download all images from paginated albums, use the manual extraction fallback method.
- **Pagination may not add new unique images.** When filtering by gallery ID, pagination page images are often duplicates of page 1 images. Check page 1 first before downloading all pagination pages.
