---
name: find-media-from-scandal-planet
description: Download media from Scandal Planet, a celebrity scandal/leak aggregation site with hosted images and videos.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# Find media from Scandal Planet

Download media from Scandal Planet (https://scandalplanet.com), a WordPress-based celebrity scandal and leak aggregation site.

## URL Patterns

- Site: `https://scandalplanet.com`
- Celebrity page: `https://scandalplanet.com/{name-slug}/` — e.g. `scandalplanet.com/charithra-chandran/`
  - Alternate patterns: `scandalplanet.com/{name}-nude/`, `scandalplanet.com/{name}-nude1/` (e.g. `kate-hudson-nude1/`)
  - Search via `?s={name}` or Google (`"{name} scandalplanet"`) if direct URL 404s
- og:image meta tag: provides a high-quality cover image (~830x850)
- Images: `scandalplanet.com/wp-content/uploads/{year}/{month}/{filename}-optimized.jpg`
  - Full-size: `-optimized.jpg` or `{filename}-scaled-optimized.jpg`
  - Gallery thumbnails: `{filename}-180x240-optimized.jpg` (remove `180x240` segment for full-size)
  - Sidebar thumbnails: `{celeb-name}-nude-145x145-optimized.jpg` (skip these — unrelated celebs)
- Videos: `scandalplanet.com/wp-content/uploads/{year}/{month}/{filename}.mp4` — direct MP4 links

## Recommendations on how to download

- Celebrity pages are single WordPress articles with embedded galleries and `<video>` elements.
- **Extract full-size images:**
  - `curl -sL "$URL" | grep -oP 'https?://[^"'"'"'<>]+\.(jpg|jpeg|png|webp)' | grep -v '180x240\|145x145'`
  - Alternatively fetch og:image meta tag for the cover image.
  - WordPress `srcset` attributes list multiple sizes (`-841x550-optimized.jpg`, `-1536x1005-optimized.jpg`, `-2048x1340-optimized.jpg`). Use `-scaled-optimized.jpg` variant if available for largest.
- **Extract videos:**
  - `curl -sL "$URL" | grep -oP 'https?://[^"'"'"'<>]+\.mp4'`
  - Videos use `<video><source src="{mp4_url}">` — direct MP4 download.
- **No auth required.** Rate limit: 0.3–0.5s between requests.
- If profile 404s, try name variations or search via `?s={name}`.

## Quality

- Images: ~60KB–3MB. Full-size typically 720–2048px wide. Hosted on their own server.
- Videos: MP4 format. Size varies. Note: some videos are truncated previews (~5s) behind a paywall overlay.
- Content mix: leaked nude/selfies, bikini/swimwear, "sextape" clips, movie scene stills.
- High value — aggregates content from multiple sources and may host unique material not found elsewhere.

## Pitfalls

- **WordPress galleries:** Full-size images are at `{filename}-optimized.jpg`. Thumbnail links use `-180x240-optimized` — you can either filter these out (they resolve correctly), or extract the `<a href>` targets which point to full-size.
- **Truncated videos:** Some videos have a paywall overlay (JavaScript pauses video at 5s). The direct MP4 download _may_ contain only the short clip. Check file size/duration after download.
- **Related celebs sidebar:** The page includes thumbnails (`-145x145-optimized.jpg`) of other celebs in a sidebar. Filter by checking if the URL contains the target celeb's name.
- **Single page per celebrity** — no pagination. All content is on one article post.
