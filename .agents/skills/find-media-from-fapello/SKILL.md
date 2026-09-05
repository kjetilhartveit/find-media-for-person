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
- **Domain note:** Only `fapello.com` is the active profile site. The `fapello.is` domain redirects unknown slugs to the homepage.
- Country-specific TLDs exist: `cz.fapello.com`, `de.fapello.com`, `es.fapello.com`, `fr.fapello.com`, `gr.fapello.com`, `hu.fapello.com`, `it.fapello.com`, `jp.fapello.com`, `nl.fapello.com`, `pl.fapello.com`, `pt.fapello.com`, `ro.fapello.com`, `ru.fapello.com`, `se.fapello.com`, `tr.fapello.com`. These are mirrors, not separate content.
- Pagination: `https://fapello.com/{slug}/page-{N}/` (~33-34 items per page, newest first)
- Profiles can have many pages (50+ for large profiles with 1,500+ items).
- Item page: `https://fapello.com/{slug}/{id}/`
- Post page: `https://fapello.com/post/{post_id}/{slug}/` — standalone posts surfaced by web search. Note: a post may exist even when the profile URL returns 404.

### Direct image download

Images can be downloaded directly without visiting item pages. The URL pattern is:

`https://fapello.com/content/{l1}/{l2}/{slug}/1000/{slug}_{ID}.jpg`

Where:

- `{l1}` and `{l2}` are the first two letters of the slug (e.g., `c/h` for `charithra-chandran`)
- `{ID}` is the sequential item ID, zero-padded to 4 digits (e.g., `0161`)
- The resolution segment changes at ID 1000:** IDs 1–999 use `1000/` in the path; IDs 1000+ use `2000/` (e.g., `content/t/y/tyla/2000/tyla_1001.jpg`).
- ID zero-padding: IDs 1–999 use 4-digit zero-padding (`0001`–`0999`); IDs 1000+ use the raw number without padding (`1000`, `1001`, etc.).

Example: `https://fapello.com/content/c/h/charithra-chandran/1000/charithra-chandran_0161.jpg`

Thumbnails on profile pages use a similar pattern with `_300px.jpg` suffix (e.g., `charithra-chandran_0161_300px.jpg`).

## Recommendations on how to download

1. **Cloudscraper for scraping**: Use Python `cloudscraper` package to bypass Cloudflare. This is the most reliable method — `gallery-dl` consistently returns 403 for Fapello. Alternatively, a headless browser (e.g., playwright, puppeteer) can also bypass Cloudflare.
2. **Manual method (primary)** — Fetch the profile page to discover the ID range. Item links are ABSOLUTE URLs in the HTML (`https://fapello.com/{slug}/{id}/`), so extract IDs with a regex like `fapello\.com/{slug}/(\d+)/` — a relative-path regex (`/^\{slug\}/\d+/`) finds nothing. ~32 items per page.
3. Check for pagination — follow `/page-2/`, `/page-3/`, etc. until pages return empty or 404. Some profiles have 50+ pages (1,500+ items).
4. Collect all unique IDs across pages. Some IDs may be missing (e.g., ID 26 on Tyla profile returned 404).
5. Download images directly using the URL formula above — no need to visit individual item pages.
6. Rate limiting: sleep 0.3–0.5s between requests. For large profiles, use parallel downloads (max 3-4 workers).
7. No authentication required.

## Media types

- Most items are JPG images. A small fraction are MP4 videos.
- To check if an item is a video, visit the item page and look for `.mp4` URLs or `<video>` tags.
- Video URLs use pattern: `https://cdn[-n1].fapello.com/content/{l1}/{l2}/{slug}/{version}/{slug}_{ID}.mp4`
  (e.g., `https://cdn.fapello.com/content/k/a/kate-hudson/2000/kate-hudson_1716.mp4`)
- The same ID may have both a `.jpg` thumbnail and an `.mp4` video — download both.

## Quality

- Images range from ~25KB to ~400KB per image (most ~55-250KB). Resolution varies: older items ~600x800, newer uploads often full-size ~1080px (e.g. 681x1024, 864x1080, 1080x1079).
- Smaller profiles (under ~150 items) tend to have smaller file sizes in the 50-100KB range and lack videos.
- Videos are typically 150KB - 12MB MP4 files in ftyp/isom format.
- Success rate is >99% — most sequential IDs resolve (Tyla: 1/1,576 missing in IDs 1-2000 range).
- Large profiles can have 1,500+ items spanning 50+ pages.
- Lots of content, consistent quality, very reliable. No auth needed.

## Pitfalls

- Some sequential IDs may be missing (404). Handle gracefully.
- **URL path segment changes at ID 1000:** IDs 1–999 use `1000/` in the content path; IDs 1000+ use `2000/`. Not accounting for this will cause 404 failures on the second half of downloads.
- The `{l1}/{l2}` path segments are derived from the slug's first two letters — verify with one known image first.
- Profile URLs may return 404 even when posts exist for the same person (found via web search at `fapello.com/post/{id}/{slug}/`).
- The `gallery-dl` fapello extractor consistently returns 403. Use cloudscraper or headless browser instead.
- Thousands of images possible — pace downloads and use rate limiting.
- Prioritize undownloaded ID ranges in follow-up sessions.
- HEAD requests to video CDN `.mp4` URLs typically fail (404) even when the video exists. Use GET requests instead.
- Profile pagination may yield overlapping IDs between pages — deduplicate when collecting IDs.
- **Phantom ID 1000**: Some profiles include item `1000` in pagination URLs (e.g., `mia-miley-1/1000/`) but the actual content never resolves (always 404). This occurs because the profile page displays `mia-miley-1/1000/` as a link in some context (related content, template artifact, etc.) but the item genuinely does not exist. When scanning IDs, verify by trying to download — skip 404 images gracefully.
- **Thread safety with cloudscraper**: `cloudscraper.create_scraper()` sessions are not thread-safe. When using parallel downloads, create a fresh session per thread (`cloudscraper.create_scraper()` called inside the worker function), not one shared session.

## Cloudflare Protection

- Fapello.com is protected by Cloudflare challenge pages.
- Simple HTTP tools (curl, wget) will get 403/CF challenge pages.
- `gallery-dl` fails with Cloudflare 403 errors.
- **Recommended**: Use Python `cloudscraper` package (`pip install cloudscraper`) — it reliably bypasses Cloudflare.
- Alternative: headless browser (playwright, puppeteer) can also bypass Cloudflare.
- Alternative domains like `fapello.net` exist but have different anti-bot systems.

## Profile Not Found

- A person may not have any content on Fapello at all.
- If the direct profile URL returns 404 AND all search variations return 0 results (verified with browser), the person is not on the platform.
- Try search variations: `{name}`, `{first}-{last}`, `{first}{last}` (no hyphen), and `{name}-1` (some profiles have numeric suffix when main slug is taken, e.g., `eleonora-bertoli-1`).
- Some people appear only via individual posts (web search for `site:fapello.com "{name}"`).
- SEO landing pages may exist at alternative slugs (e.g., `fapello.com/elebertoli/`) but return 200 with no actual items — only the profile slug with content matters.
- `/feed/{id}/` URLs are curated/featured feed pages linking to profiles, not standalone profiles themselves.
- **Identity verification cues**: Profile and item pages carry no bio or description text (no meta description either). The slug, profile title, and the social links embedded in the profile page (e.g., an OnlyFans URL) are the main signals that the profile belongs to the right person. Cross-check those handles against external sources (web search, IMDb) before downloading.

### Fapello Internal Search Doesn't Work

- The Fapello internal search (`fapello.com/search_v2/{query}/`) does not return results even when content exists. The search page loads but shows 0 items.
- **Use external search instead**: Google or Bing site search (`site:fapello.com "{name}"`) to find the correct profile URL.
- Search results show the full profile title (display names + tags) in the page title, which helps identify the correct profile.
- **Alternate/primary names**: Profile titles may show an alternate primary name followed by the searched name (e.g., "Lupe Burnett / Megan Vale Nude Leaks"). The slug uses the searched name but the primary display name may differ.

### Video Items

- Some items are videos (MP4) and have both a `.jpg` thumbnail and `.mp4` video file.
- The `.jpg` file is the thumbnail; the `.mp4` is the actual video. Download both when available.
- Video CDN URL: `https://cdn.fapello.com/content/{l1}/{l2}/{slug}/{version}/{slug}_{ID}.mp4`
- The video CDN may return a 302 redirect with a time-limited token — follow redirects.
- **HEAD requests to video CDN URLs typically return 404 even when the video exists.** Use GET requests to check and download.
- Videos tend to cluster in the upper end of the ID range (near the end of the profile). For a profile with 1,500+ items, videos were found at IDs ~1,495-1,575.
- To find videos efficiently for large profiles: iterate through all IDs and try downloading `.mp4` files with GET requests (404 = no video, 200 = valid video). Videos typically range from ~150KB to ~12MB.

### Small Profiles

- Some profiles are very small (e.g., Kylie Jenner has only 14 items).
- For small profiles, pagination may return the same items on all pages — deduplication is still needed, but you'll quickly see the profile is small.
- Small profiles have no videos and only one page of real items.
- Profile URL slug variations: try `{first}{last}` (no hyphen, e.g., `kyliejenner`), `{first}-{last}`, and `{name}-1`.
- **Non-sequential IDs in small profiles**: Even small profiles may have non-sequential IDs (e.g., IDs 1-4 and 1000). Always check item pages for actual content rather than assuming sequential density means completeness.
- Item pages can reference item IDs not present in the profile page's own URL list (e.g., a direct `…/content/{l1}/{l2}/{slug}/…/{slug}_{ID}.jpg` reference in next/related UI). After scanning, probing a few IDs past the max confirmed ID is cheap insurance (1 GET each) and can find the last items of a profile.
- **Gap IDs can still resolve**: IDs that never appear in the profile's pagination links (gaps inside the ID range, or just past the max) may still return 200 via the direct content URL — sometimes just a small ~300x300 placeholder instead of full size. Probing gap IDs is cheap insurance; check returned dimensions and keep them if unique.

### Pagination Cycling (Medium Profiles)

- Medium-sized profiles (e.g., Maya Bijou with ~110 items, 4 unique pages): pages beyond the unique content cycle — they return the same items repeatedly (e.g., pages 5+ show the same 32 items).
- Detect unique pages: stop scanning pages when the max ID no longer decreases between consecutive pages (page n max_id == page n+1 max_id means page n+1 is cycling).
- Alternatively, stop when you've seen the same set of IDs twice.
- Example: Maya Bijou (maya-bijou-1) has IDs 1-111 (missing 38 = 110 items). Pages 1-4 have different IDs; pages 5+ cycle the same 32 items.
- This cycling pattern means scanning the full 50 pages of a small profile without deduplication is wasteful.

### Multiple Slugs for Same Person

- Multiple profile slugs may exist for the same person with DIFFERENT content (not just duplicates). Example: `laylajenner` (135 images, IDs 63-197) and `thelaylajenner` (6 images, IDs 1-6) — both for the same person, different l1/l2 URL paths (`l/a` vs `t/h`), completely non-overlapping images.
- After downloading from one slug, try alternate slugs (e.g., prefixed with `the`) by checking the profile page title for alternate names. The title often lists alternate display names (e.g., "laylajenner / thelaylajenner Nude Leaks OnlyFans - Fapello").
- When checking alternate slugs, use the correct l1/l2 path segments derived from the alternate slug's first two letters. Small profiles (<20 items) don't have videos.
- **Multi-alias combined slugs**: Fapello also hosts slugs that combine several aliases of the same person with word separators (e.g. `{handle}-{alias1}-o-{alias2}`), mirroring naming used by FapMenu/Fapeza. These can contain additional content that is entirely non-overlapping with the per-alias slugs. Check such combined slugs when a person is known under multiple names, and always dedupe by hash across all slugs.
