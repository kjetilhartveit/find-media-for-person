---
name: find-media-from-scandal-planet
description: Use when you need to find and download media from Scandal Planet, a celebrity scandal/leak aggregation site with hosted images and videos.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for media of a specific celebrity on Scandal Planet
- Downloading leaked content, bikini photos, or media from their galleries
- Scraping images and videos from a celebrity article page on Scandal Planet

# Find media from Scandal Planet

Download media from Scandal Planet (https://scandalplanet.com), a WordPress-based celebrity scandal and leak aggregation site.

## URL Patterns

- Site: `https://scandalplanet.com`
- Celebrity page: `https://scandalplanet.com/{name-slug}/` — e.g. `scandalplanet.com/charithra-chandran/`
  - Alternate patterns: `scandalplanet.com/{name}-nude/`, `scandalplanet.com/{name}-nude1/` (e.g. `kate-hudson-nude1/`)
  - URL slugs may have numeric/year suffixes (e.g. `bella-thorne-2023new`, `megan-thee-stallion2`) — often indicates renamed/recycled slugs or multiple versions.
  - Name variations may redirect (e.g. `megan-thee-stallion`, `megan-thee-stallion-nude`, `megan-thee-stallion-nude1` all redirect to `megan-thee-stallion2/`)
  - Search via `?s={name}` or Google (`"{name} scandalplanet"`) if direct URL 404s
- og:image meta tag: provides a high-quality cover image (~830x850)
- Images: `scandalplanet.com/wp-content/uploads/{year}/{month}/{filename}-optimized.jpg`
  - Full-size: `-optimized.jpg` or `{filename}-scaled-optimized.jpg`
  - Gallery thumbnails: `{filename}-180x240-optimized.jpg` (remove `180x240` segment for full-size)
  - Sidebar thumbnails: `{celeb-name}-nude-145x145-optimized.jpg` (skip these — unrelated celebs)
- Videos: `scandalplanet.com/wp-content/uploads/{year}/{month}/{filename}.mp4` — direct MP4 links

## Recommendations on how to download

- Celebrity pages are single WordPress articles with embedded galleries and `<video>` elements.
- **Extract full-size images (robust method):**
  - WordPress `srcset` attributes contain multiple sizes per image. Use a more precise extractor rather than raw grep to avoid duplicates.
  - Python extraction approach: parse `<img>` tags with `wp-image-` class, get `src` and prefer `-scaled-optimized.jpg` or non-resized `-optimized.jpg` URLs. Filter out `145x145`, `180x240`, `295x295` thumbnails and intermediate sizes (`-\d+x\d+-optimized`).
  - Alternative: use gallery-dl with `--config` pointing to a custom extractor config.
  - Alternatively fetch og:image meta tag for the cover image.
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
- **No content for celebrity**: Some celebrities are not covered — Scandal Planet only features a subset (~100-120) of A-list celebrities. If the site returns zero results after thorough searching, the celebrity may not be featured.
- **Redirect (301) for non-existent profiles**: URL variations for non-existent celebrity profiles (e.g. `scandalplanet.com/nonexistent/`) will 301-redirect to the homepage rather than returning a 404. This is distinct from a profile that exists with no content. Use search (`?s=query`) as the definitive check.
- **Redirect to Angelina Jolie for "Jolie" names**: Any URL slug containing "jolie" will 301-redirect to Angelina Jolie's page (`scandalplanet.com/angelina-jolie/`). This is a site-wide rule that applies to any URL containing that substring. A search for "jenaveve jolie" returns "Nothing Found" rather than redirecting. Use site search or Google as the definitive way to check for coverage.
- **Rising/young celebrities may not be covered**: Newer or younger celebrities without major scandal history may not have articles. The site focuses on established A-list celebrities with scandal/leak history.
