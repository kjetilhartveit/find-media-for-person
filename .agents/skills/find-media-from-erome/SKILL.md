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

- Image quality is modest: files range from ~24KB to ~167KB.
- Resolutions are typically 480–576px wide, with occasional higher-res images (up to 1280×720 observed).
- No videos observed in some albums — content is image-heavy.
- Content quality varies by uploader; search results are limited per person.

## Pitfalls

- Album pages may be behind Cloudflare protection in some cases.
- Erome filenames are random IDs — no semantic naming for downloaded files.
- Search results per person may be limited (only 2 albums found for "Charithra Chandran").
- Some albums may have duplicate images shared across albums.
