---
name: find-media-from-erome
description: Download media from Erome, a user-hosted adult content sharing site with albums.
---

# Find media from Erome

Download images and videos from Erome (https://www.erome.com), a user-hosted adult content sharing platform.

## URL Patterns

- Site: `https://www.erome.com`
- Album pages: `https://www.erome.com/{album_id}` (e.g., `erome.com/fer6Kjy4`)
- Search for celebrity name to find relevant albums

## How to Download

1. Search for the celebrity name on the site to find relevant albums.
2. Open each album page to extract media.
3. **Parse the album page HTML** to extract actual full-size image URLs — do not guess the URL pattern.
4. The common approach of removing `/thumbs/` from thumbnail URLs **does not work reliably** for most albums.
5. Rate limiting: sleep 0.3–0.5s between requests.

## Quality

- Images range from ~29KB to ~196KB.
- 3/10 — good content exists but download method is unreliable. Many albums fail due to the URL pattern mismatch.
- Albums have engagement metrics (likes, views) to gauge popularity.

## Pitfalls

- **Full-size URL pattern fails.** The `/thumbs/` removal trick doesn't work for most albums. Always parse the album page for the actual full-size URL.
- Album pages may be behind Cloudflare protection.
- Many URLs return HTML (not images) when the URL pattern is guessed incorrectly.
- Content quality varies by album uploader.
