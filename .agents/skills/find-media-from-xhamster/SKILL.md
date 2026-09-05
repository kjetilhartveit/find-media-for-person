---
name: find-media-from-xhamster
description: Use when downloading media from XHamster profiles and content.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Downloading videos from XHamster user profiles
- Extracting galleries from XHamster
- Scraping pornstar pages on XHamster

# Find media from XHamster

XHamster is an SPA, but much useful data is embedded in the initial HTML as escaped JSON. Standard HTTP requests (requests/urllib) can extract significant data without browser automation.

## URL Patterns

- **Profile**: `xhamster.com/pornstars/{name}`
- **Search**: `xhamster.com/search/{name}`
- **Gallery**: `xhamster.com/photos/gallery/{id}`
- **User galleries**: `xhamster.com/users/{handle}/photos`
- **User videos**: `xhamster.com/users/{handle}/videos`
- **Single video**: `xhamster.com/videos/{slug}-{id}`
- **Shorts**: `xhamster.com/shorts/{slug}-{id}`

## Method 1 — Embed JSON from profile page

Request `https://xhamster.com/pornstars/{name}` with a normal User-Agent. The response HTML is large (~300KB) and contains:

- Profile avatar in CSS: `landing-info__logo-image` with `background-image: url('...')` URL at `https://ic-tt-nss.xhcdn.com/.../avatar1.jpg`
- **NOTE**: On many profile pages (e.g., Amber Hardin), the videoThumbProps array contains *"best trending"* videos, NOT the pornstar's own videos. Only a few may actually feature the person. Use search results (Method 2) for comprehensive video discovery.
- `videoCount` — total video count for the pornstar (small field, easy to grep)
- `videoThumbProps` appears multiple times; on profile pages the **first** large array (~36 items) is a site-wide "trending" block shared across pages, and a second, smaller array matching `videoCount` holds the pornstar's actual videos. Always take ALL arrays and dedupe by `id`.
  - Each item has: `id`, `title`, `pageURL`, `created`, `duration` (seconds), `views`, `thumbURL`, `imageURL`, `trailerURL`
  - Filter by checking if the person's name or known aliases appear in `title` or `pageURL`
- `momentsListComponent` — contains `videoThumbProps` for short videos/clips

To extract reliably, use `json.JSONDecoder().raw_decode()` on each occurrence of `"videoThumbProps"\s*:\s*\[` (hand-rolled bracket counting is fragile on these payloads). No `\/` unescaping needed before `raw_decode`.

**Multiple profiles for one person**: a performer with multiple stage names can have separate `/pornstars/` pages (each with its own `videoCount`). Search all known aliases and merge the lists; profiles also occasionally contain mis-categorized videos whose titles don't mention the person — verify by title before downloading.

## Method 2 — Search page (best for video discovery)

Request `https://xhamster.com/search/{name}` with normal User-Agent. Contains:

- `searchResult` JSON object with `"videoThumbProps"` array (~47 videos per page)
- Separate `"videosList"` section with `"props"` containing another `videoThumbProps` array
- Search results are the **primary source** for finding all videos of a person, as profile pages may show trending/irrelevant content.

Thumbnail URLs are at `https://ic-vt-nss.xhcdn.com/` with quality suffixes like `s(w:1280,h:720),webp` and paths like `/005/748/041/v2/2560x1440.268.webp`. The `imageURL` field (`s(w:1280,h:720)` variant) downloads fine directly with plain requests — no Referer needed. Only the small variants (`s(w:350,h:620)`, `s(w:526,h:298)`) return 403 Hotlink Forbidden.

## YouTube-dl download (videos)

Videos are served via HLS (m3u8). Use:
```bash
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "output.mp4" "https://xhamster.com/videos/{slug}-{id}"
```

To cap quality (e.g. max 720p, to keep downloads small), a robust chain is:
```bash
yt-dlp -f "bestvideo[height<=720]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720][ext=mp4]/best[ext=mp4]/best" ...
```

Best quality is 1080p MP4. Videos average 170-200MB but some reach 600-800MB+. yt-dlp automatically applies `FixupM3u8` to fix MPEG-TS in MP4 containers. Each download takes roughly 2-5 minutes at typical bandwidth.

## Technical Tips

- Use User-Agent: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36`
- Video thumbnails: `https://ic-vt-nss.xhcdn.com/` (no Referer needed for the `s(w:1280,h:720)` `imageURL` variant)
- Photo images: `https://ic-ph-nss.xhcdn.com/`
- Avatar/profile images: `https://ic-tt-nss.xhcdn.com/`
- Short video trailers: `https://thumb-v*.xhcdn.com/`
- JSON in HTML uses `\/` not `/` — must `.decode('unicode_escape')` before `json.loads()`
- The `imageURL` field often has higher resolution than `thumbURL`
- Profile pornstar pages often link to user channels (e.g., "Thai Swinger") that host the same content under a different uploader

Search results are paginated (up to 22+ pages for popular stars, each page ~47 videos). Pagination details:

- Extract ALL `videoThumbProps` array occurrences per page (regex for `"videoThumbProps"\s*:\s*` and bracket-counting each) and merge by `id` — the first occurrence may be a shared trending/related block that is identical across pages, which silently breaks pagination if you only take the first array.
- Pagination is driven by a `pagination` JSON block: `{"active":1,"next":2,...,"maxPages":N,"pageLinkTemplate":"https://xhamster.com/search/{query}?page={#}"}`. **Use the URL from `pageLinkTemplate` for pages 2..maxPages** — the template uses `+`-encoded query names (e.g. `lela+star`). Requesting `?page=N` against a differently-encoded slug (e.g. `lela-star`) is silently ignored and returns page 1 repeatedly.
- The search `total` field should equal the profile's `videoCount` — a good completeness check.
- Compare video IDs against the profile list to find extras. Search results may include videos where the model is featured but the name is not in the title (only ~1/2 of results mention the name in title/URL, the rest match via tags).

## Method 3 — Individual video pages

Request `https://xhamster.com/videos/{slug}-{id}`. The `og:image` meta tag contains the same high-quality thumbnail URL as the JSON `imageURL` field (1280x720 webp from 2560x1440 source) — verified identical. So to collect thumbnails for hundreds of videos, use `imageURL` from the profile/search JSON directly instead of fetching every video page (saves one HTTP request per video).

## Method 4 — Photo galleries

Request `https://xhamster.com/photos/gallery/{id}`. Images are served from `https://ic-ph-nss.xhcdn.com/` with URLs like:
```
https://ic-ph-nss.xhcdn.com/a/{hash}/webp/000/517/456/852_1000.
```

Filter out 32x32 tiny thumbnails. Look for URLs containing `1000`, `852`, `1280` which indicate full-size photos.

Methods 1-4 work with plain `requests`/curl — no browser automation or cookies needed for thumbnails, metadata, OR full video downloads (yt-dlp handles the HLS streams fine). Note the search `total` can be misleadingly large (multi-word queries are loosely matched and return thousands of videos of unrelated people sharing the same first/last name); the profile `videoCount` is the figure to beat for completeness.

## Methods That Fail

- **gallery-dl**: No `pornstars` extractor. Has `XhamsterGalleryExtractor` and `XhamsterUserExtractor` only. Does not support `/videos/` pages for this purpose.
- **yt-dlp**: Returns "Unsupported URL" for `/pornstars/` and `/users/` pages (returns 0 videos). Only works for `/videos/{slug}-{id}` pages via the `XHamster` extractor.

## Pitfalls

- **Profile page shows trending videos**: The `/pornstars/{name}` page often shows "best trending" videos, not the pornstar's own content. The `videoThumbProps` array may only include a few relevant videos. Always use search (`/search/{name}`) as the primary discovery method.
- **JSON escaping**: Embedded JSON in HTML has all `/` escaped as `\/` — must unescape before parsing
- **Limited video list on profile**: The `videoListProps` array on the main profile page only includes the first page of videos. Search page discovery finds additional videos not in the profile list
- **Thumbnail hotlink protection (partial)**: Small thumbnail variants (`s(w:350,h:620)`, `s(w:526,h:298)`) return 403 Hotlink Forbidden when fetched directly, but `imageURL` (`s(w:1280,h:720)`) downloads fine without a Referer — same quality as video page og:image. No need to fetch per-video pages for thumbnails.
- **Pagination**: Search results have many pages (e.g., 22+ pages for popular stars). Use the `pageLinkTemplate` URL from the page's `pagination` JSON (it uses `+`-encoded query names) for `?page=N` — other encodings can silently return page 1 repeatedly. Deduplicate by video ID. Search `total` should equal the profile `videoCount`
- **Placeholder thumbnails**: Some og:image URLs are generic placeholders — verify by checking if the URL or title references the target person
- **Aliases**: Search using known aliases — a model may appear under different names (e.g., "Lera" appears in "Amber Hardin" search results)