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

### gallery-dl config for Pictoa (to control output format)

Create a JSON config file for fine-grained output control:

```json
{
  "extractor": {
    "base-directory": "<output-dir>",
    "sleep-request": [0.4, 0.8],
    "pictoa": {
      "directory": ["{album_id} {album_title}"],
      "filename": "{id}.{extension}"
    }
  }
}
```

Key variables for Pictoa: `album_id`, `album_title`, `id`, `extension`, `filename` (hash). Use `--restrict-filenames windows` for Windows-compatible filenames. The per-album `{album_id} {album_title}` subfolder keeps albums organized and avoids name collisions; drop the `directory` key to dump everything flat.

### Batch-downloading many albums

For a large number of albums:

- Pass ALL album URLs in one `gallery-dl` invocation together with `--download-archive <file>.sqlite` so re-runs/continuations skip already-finished files.
- Run it in the background (e.g. `nohup ... > batch.log 2>&1 &`) and poll the log — ~1000+ images with a 0.4-0.8s sleep finishes in ~5-10 min.
- Verify afterwards: per-album file count vs the photo count shown on the search results page; a shortfall means the album is paginated (see fallback).

### gallery-dl known limitations for Pictoa

- gallery-dl only downloads page 1 of paginated albums. For paginated albums, use the manual extraction fallback method.
- gallery-dl does NOT support pagination URLs (`-p2.html`, `-p3.html` returns "Unsupported URL").

## Fallback download method — Manual album page parsing

When `gallery-dl` is unavailable or fails:

1. Search using the `/s/<query>/` URL pattern. Try multiple query variations including name spelling variants (e.g. "arya fae" AND "arya faye"). Try full name, handle, performer name.
2. Also try category URLs like `/c/<celebrity-name>-<category-id>/`.
3. Parse search results for album links matching `https://www.pictoa.com/albums/...html`. Filter for relevance — generic name searches may return unrelated adult performers with similar names (e.g., "Anissa Kate" mixed in with "Kate Hudson"). Group albums with other models (e.g., "Arya Fae and Jill Kassidy", "Arya Fae and Bailey Brooke") are relevant if they contain the target person.
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
- Category URL pattern: `https://www.pictoa.com/c/<name>-<category-id>/` — celebrity category pages list all albums the site attributes to that person. Find the numeric category ID via Google `site:pictoa.com/c/ <name>` (or any indexed album page of the person linking to it). Category pagination WORKS (unlike search): `/c/<name>-<id>/page2.html`, `/page3.html`, ... — page size ~72 albums.
- Search pagination: `https://www.pictoa.com/s/<query>/p2/` — NOTE: p2 pagination was observed NOT to work (returns 404). Only use first page of search results.
- Image CDN: `t1.pictoa.com` — serves actual full-size images (commonly ~100-200KB JPEG). Use these URLs as-is.
- NOTE: `s2.pictoa.com` previously served high-quality versions by swapping `t1` → `s2` in URLs. As of 2026-07-18 this CDN returns 404. Only `t1.pictoa.com` works.
- Example image URL: https://t1.pictoa.com/media/galleries/164/015/164015593e5b1db71d5/2919079593e5b1dba2c5.jpg
- **Image URL structure for filtering:** `https://t1.pictoa.com/media/galleries/<dir>/<gallery_id><random_hex>.<ext>`. The gallery ID (e.g., `132450`) appears as a prefix in the filename after the directory name (e.g., `1324505498958d9d727.jpg`). Filter related gallery images by checking the image URL contains the directory path (`/media/galleries/<dir>/`) AND the gallery ID in the filename. Directory path can be extracted from the album page title or matched via the gallery ID in the first path segment.

## Quality

- The `t1` CDN serves actual full-size images (not thumbnails). A recent run averaged ~150KB/file at 683x1024.
- File size varies by gallery; generally ~100-200KB JPEG per file.
- This is the highest quality Pictoa offers — the `s2` high-res CDN is broken (see below).

## Pitfalls

- **Search requires `/s/<query>/` URL format.** Old patterns (`/search/<q>.html`, `/search?query=<q>`) return 404.
- **No direct celebrity URLs via search — but celebrity category pages exist.** `/c/<name>-<id>/` pages are the site's per-person album list (find the ID via Google `site:pictoa.com/c/ <name>`). They are the most complete enumeration of a person's albums and have working `/pageN.html` pagination. CAVEAT: categories are loose keyword matches and mix in OTHER people sharing a name — one observed category held 1500+ albums where the target person was a small fraction (e.g. "selena-spice-15885" mixed albums of Selena Gomez, Selena Rose, "Cierra Spice", "Bella Spice" etc.). Never assume category membership = identity; filter with the identity signals below.
- **Album-page meta keywords are the site's per-album celebrity classification.** The `keywords` meta on an album page starts with the celebrity the site attributes it to (e.g. `selena spice,amateurs,latinas,...`) even when the album title drops the full name (e.g. titled "Selena in baggy cloths"). This is a strong identity signal for alias-era content. The related-album link rows are NOT a trustworthy signal — they link other people sharing only a name token (e.g. other "X Spice" models next to "Selena Spice").
- **Dedupe an album against an existing archive by numeric image ID.** If a prior run used gallery-dl `{id}.{extension}` naming, local filenames ARE the PictOA image IDs (the number in `/albums/<slug>-<aid>/<img-id>.html`). To skip an already-captured album: fetch the page, extract that album's own image links (see next pitfall), and check whether all IDs exist locally. No need to re-download or visually verify.
- **Album's own images vs related-gallery links.** The album's own image links are `https://www.pictoa.com/albums/<slug>-<aid>/<img-id>.html` (or `-<slug>-p2/` on later pages) where the slug ENDS with the album's full numeric ID; related-gallery links point at different slugs/IDs. Match slugs ending in the full album ID (regex: `albums/[^"]*<aid>(?:-p\d+)?/(\d{6,10})\.html`). The same split holds for CDN URLs: filenames start with the album ID.
- **CDN URL path has THREE segments before the filename.** `t1.pictoa.com/media/galleries/<a>/<b>/<18-hex>/<album_id><11-hex>.jpg` — e.g. `.../galleries/266/898/2668986402b1495e69b/40871946402b14b6d425.jpg` (album 4087194). Filenames: 6-7 digit album ID prefix + 11 hex.
- **Relevance filtering is important.** A simple name search (e.g. "jessi") may return unrelated performers sharing the same name. Try adding disambiguating terms (handle, full name, performer name). Searching "sofie" alone returns 100+ albums of adult performers — not the celebrity you want.
- **Searching without last name returns many misspellings.** Searching just "Collien" returned albums titled "Collien Fernandez" (misspelled), "Collien Fernandez und Palina Roijinski", and ghostface-related content that isn't the target person. Always use the full name when possible, then manually vet results.
- **Search result photo counts are unreliable.** The album page image count may differ significantly from what the search result shows. The "Collien Fernandes" search listed album 44726 as having 41 photos, but the actual page had 53. Fetch each album page to get the real count.
- **Related gallery images on every album page.** Album pages show a row of related/recommended gallery thumbnails at the bottom. These also use `data-lazy-src` with `t1.pictoa.com` URLs. Filter by ensuring the gallery ID appears in the image URL path.
- **POST to search-by-form redirects but -L fails.** The CSRF POST to `/search-by-form` returns a 302 redirect, but following it with `-L` may return 405. Get cookies, POST to populate session, then GET the search URL directly with those cookies.
- **The `s2` CDN is broken.** The former advice to swap `//t1.` → `//s2.` for higher quality no longer works and returns 404 — use `t1` URLs as-is.
- Labor-intensive: one page fetch per album to extract all image URLs.
- **No "No Results" indicator on empty search.** A search returning no albums shows `No Results` in the page body but still returns a 200 status code — check the HTML for `<p id="noResults">` or search returns 404.
- **Search returns 404 for non-existent queries.** If the search query has no results, the search URL may return 404 (not just 200 with No Results text).
- **Gallery ID regex.** Album names contain dashes, so `[^-]+` pattern won't work. Use regex like `(\d{6,7})` to extract the gallery ID — IDs can be 6 or 7 digits (e.g., `inna-dinamica-171104.html` has 6-digit ID, `inna-outdoor-3803809.html` has 7-digit ID). For nested paths use `albums/.*?-(\d{6,7})/\d+\.html`.
- **Two album URL formats.** Some album links have a trailing `/image-id.html` (e.g., `/albums/kate-hudson-booty-3228997/75141781.html`). Extract the last number (6 or 7 digits) before `.html` in the URL as the gallery ID.
- **Image filtering by gallery ID.** The gallery ID must be in the image URL path on the album page to filter out related gallery thumbnails. Album pages include `data-lazy-src` images from related/recommended galleries — only keep URLs containing the target gallery ID. Gallery IDs in image URLs may have extra characters appended (e.g., `102839` appears as `102839549719b9df82b` in the filename). Filter by checking the gallery ID also appears in the directory path of the CDN URL (`/media/galleries/<DIR>/<GALLERY_ID><random>.jpg`). Related gallery images will have a different directory number.
- **gallery-dl does not support pagination URLs.** Passing `-p2.html`, `-p3.html` etc. to gallery-dl returns "Unsupported URL". The extractor only handles the main album URL (`-p1.html` implicitly). To download all images from paginated albums, use the manual extraction fallback method.
- **Pagination may not add new unique images.** When filtering by gallery ID, pagination page images are often duplicates of page 1 images. Check page 1 first before downloading all pagination pages.
- **One album can have multiple localized slugs — dedupe by album ID.** The same album ID appears under several title slugs in different languages (e.g. an English, Spanish and French slug all pointing to the same `-2646856.html` ID). Album pages even list their localized siblings. When building an album list, key on the numeric album ID, not the slug.
- **Verify identity from metadata when you can't view images.** If your tooling has no image input, confirm an album is really the person by matching its meta tags (hair color, ethnicity, tattoos, "pornstar"/"latina" etc.) against known facts about the person, and by noting multi-model albums that pair the target with known performers — those shared shoots are a strong identity signal.
- **CDN image filenames embed a hex Unix timestamp.** In the filename `<album_id><11-hex>.jpg`, the first 8 hex digits of the 11-hex suffix (i.e. right after the album ID) are a Unix timestamp (e.g. suffix `6402b14b6d425` → `6402b14b` ≈ 2023-04-07). Do NOT use the hex from the directory path segment — that's a different value. Decode to estimate how old the source content is and sanity-check that an album matches the person's active era.
- **Search result photo counts are usable as download-size estimates** (they live in small count spans next to each album block), but fetch the album page for the exact number (counts are often off by a few).
