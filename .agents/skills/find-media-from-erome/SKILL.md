---
name: find-media-from-erome
description: Use when you need to find and download media from Erome, a user-hosted adult content sharing site with albums.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for albums of a specific person on Erome
- Searching Erome user pages for media
- Searching Erome by query to find albums matching a person
- Downloading images and videos from Erome albums or user pages

# Find media from Erome

Download images and videos from Erome (https://www.erome.com), a user-hosted adult content sharing platform.

`gallery-dl` has a built-in `EromeAlbumExtractor`, `EromeUserExtractor`, and `EromeSearchExtractor` — use this as the **primary** download method. Fall back to manual parsing only when `gallery-dl` fails.

## URL Patterns

- Site: `https://www.erome.com`
- Search: `https://www.erome.com/search?q={name}`
- Album pages: `https://www.erome.com/a/{album_id}` (e.g., `erome.com/a/fwBHXEGc`)
- User pages: `https://www.erome.com/USER`
- Media served from: `https://s{number}.erome.com/{user_id}/{album_id}/{file_id}.jpg`

## Primary download method — Download via gallery-dl

`gallery-dl` handles Erome natively with 3 extractors: `EromeAlbumExtractor`, `EromeUserExtractor`, `EromeSearchExtractor`. It resolves all media URLs, filters thumbnails, and downloads files with no auth required.

## Fallback download method — Manual parsing and download

When gallery-dl is unavailable or fails:

1. **Search** for the person's name on `https://www.erome.com/search?q={name}` — results include album cards with titles and engagement metrics. Look for album links matching `/a/{album_id}`.
2. **Parse album pages**
   - Extract `data-src` and `src` attributes from `<img>` tags — these point directly to full-size media on `s{number}.erome.com`.
   - Filter out any URLs containing `/thumbs/` — those are thumbnails.
   - No URL pattern guessing needed; the `data-src`/`src` attributes provide the actual full-size URLs directly.
3. **Download media** with `Referer: https://www.erome.com/` header and rate-limit to 0.3–0.5s between requests.
4. Prefix filenames with the album ID to avoid collisions (Erome files have random IDs).

## Quality

- **Images**: modest quality, files range from ~24KB to ~250KB, typically 480–576px wide, occasional higher-res (up to 1280×720 observed).
- **Videos**: typically 720p quality, can be large (1MB–240MB+). Videos are served from `v{number}.erome.com` with `_720p.mp4` suffix.
- Content quality varies significantly by uploader.
- Some content is from dedicated content creators/farms (e.g., "Gloryhole-Top-Secrets", "Gangbang-Creampie-Secrets", "PrettyDirtySluts") that post multiple albums per person.

## Known Sources with High-Value Content

- **Gloryhole-Top-Secrets**: Posts multiple albums per person focusing on facial/cumshot content.
- **Gangbang-Creampie-Secrets**: Post gangbang/creampie themed content.
- **PrettyDirtySluts**: Posts explicit solo/couple content.
- **ESPOSASAFADINHA**: Posts leaked/personal content.
- **GoingOutofBusiness**: Posts studio/performance content.
- **TheWatcher77**: Posts celebrity content in "Keep the Beat" themed albums.
- **tcr31**: Aggregator with bulk celebrity albums.
- **BlackTittyBear**: Posts celebrity content in dedicated albums.
- **djkidrich**: Posts large collections (100+ images) of celebrity content.
- **Digitaldash**: Posts celebrity PMV and edited content.
- **Celebs_Trending**: Posts trending celebrity content with emojis in titles.

## Search Strategy & Pitfalls — Updated 2026-08-13

- **No dedicated user profiles for most celebrities**. User pages like `erome.com/megantheestallion`, `erome.com/megan_stallion` return 404 even when album links are visible in page HTML. Do NOT rely on gallery-dl User extractor for celebrities.
- **Erome search returns false positives**. Search results include unrelated albums (other celebrities, general content). After downloading, filter by filename/album title containing the person's name.
- **Erome search is unreliable**. The `EromeSearchExtractor` and even direct HTML search often return "No results" for model names even when a matching user page exists. Try multiple search queries: `query`, `first+last`, `firstlast` (no space), and variations.
- **gallery-dl User extractor can fail** with 404. If the user URL fails, download individual albums using their IDs extracted from the HTML.
- **Album titles may use abbreviations** like "Meg" or "Megs". Check both full name and common abbreviations when filtering.
- **Gallery-dl search downloads batched albums** (~20-30 per run). For larger result sets (50-100+ albums), split URL lists into batch files and process sequentially.
- **Pagination**: User pages typically have multiple pages. Check `?page=2`, `?page=3`, etc. to get all albums.
- **Gallery-dl gallery directory config**: Don't use nested dict config for archive (e.g., `{'archive': {'file': '...'}}`); use flat string format.

## Download Filtering Tips

- After downloading, filter files by checking filename for the person's name.
- Remove incomplete downloads (.part files) after filtering.

## Pitfalls

- Album pages may be behind Cloudflare protection in some cases.
- Erome filenames are random IDs — no semantic naming for downloaded files.
- Search results per person may vary widely in quantity (2–9+ albums observed).
- Some albums may have duplicate images shared across albums.
- Video downloads can be slow due to file sizes; consider rate-limiting for large batches.
- Gallery-dl search downloads handle all albums at once; individual album downloads can be used for targeted fetching.
