---
name: find-media-from-erome
description: Download media from Erome, a user-hosted adult content sharing site with albums.
---

# Find media from Erome

Download images and videos from Erome (https://www.erome.com), a user-hosted adult content sharing platform.

## URL Patterns

- Site: `https://www.erome.com`
- Search: `https://www.erome.com/search?q={name}`
- Album pages: `https://www.erome.com/a/{album_id}` (e.g., `erome.com/a/fwBHXEGc`)
- Media served from: `https://s{number}.erome.com/{user_id}/{album_id}/{file_id}.jpg`

## How to find and download media

1. **Search** for the person's name on `https://www.erome.com/search?q={name}` — results include album cards with titles and engagement metrics.
2. **Parse album links** from the search results HTML. Look for `class="album-link"` attributes containing `href` with the album URL (e.g., `/a/fwBHXEGc`).
3. **Fetch each album page** and extract media URLs:
   - Extract `data-src` and `src` attributes from `<img>` tags — these point directly to full-size media on `s{number}.erome.com`.
   - Filter out any URLs containing `/thumbs/` — those are thumbnails.
   - No URL pattern guessing needed; the `data-src`/`src` attributes provide the actual full-size URLs directly.
4. **Download media** with `Referer: https://www.erome.com/` header and rate-limit to 0.3–0.5s between requests.
5. Prefix filenames with the album ID to avoid collisions (Erome files have random IDs).

## Quality

- Image quality is modest: files range from ~24KB to ~167KB.
- Resolutions are typically 480–576px wide, with occasional higher-res images (up to 1280×720 observed).
- No videos observed in some albums — content is image-heavy.
- Content quality varies by uploader; search results are limited per person.

## Pitfalls

- Album pages may be behind Cloudflare protection in some cases.
- Erome filenames are random IDs — no semantic naming for downloaded files.
- Search results per person may be limited (only 2 albums found for "Charithra Chandran").
- Some albums may have duplicate images shared across albums.