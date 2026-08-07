---
name: find-media-from-aznude
description: Use when you need to find and download media from AZNude, a celebrity nude content aggregator with hosted images and embedded videos.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for media of a specific celebrity/person on AZNude
- AZNude has dedicated pages per celebrity

# Find media from AZNude

Download media from AZNude (https://www.aznude.com), a celebrity nude content site with dedicated pages per celebrity.

## URL Patterns

- Site: `https://www.aznude.com`
- Celebrity page: `https://www.aznude.com/view/celeb/{initial}/{slug}.html` — first letter + lowercase slug (e.g., `aznude.com/view/celeb/c/charithrachandran.html`)
- Images from CDN: `cdn2.aznude.com/{slug}/{category}/{filename}.jpg`
- User uploads: `user-uploads.aznude.com/data/azncdn/{hash}/{hash}.jpg` (full-size) and `user-uploads.aznude.com/data/thumbs/{hash}/{hash}.jpg` (thumbnails)
- Video thumbnails: `cdn2.aznude.com/antibandit/{slug}/{category}/thumb3_{name}.jpg`

## Recommendations on how to download

- **Direct celebrity page** — URL format is predictable: first letter of name + name slug. Try variations if 404s.
- **Extract media URLs** using `curl | grep`:
  - Download full-size images from `data/azncdn/` paths (not `data/thumbs/`).
  - Download `cdn2.aznude.com/{slug}/` images (not `/antibandit/` thumbnails).
  - Filter out `/images/categories/` (category icons), `/sparkthumbs/`, and biopic images of unrelated celebs.
- **No auth required.** Rate limit: sleep 0.3–0.5s between requests.
- Some celeb pages may have 404 if no content exists — try slug variations.

## Quality

- Images: ~100KB–3MB. Resolutions vary, user-uploads and CDN images both decent quality.
- Content: mix of leaked photos, bikini/swimwear, scene stills from movies.
- Moderate value per celeb. Content may be sourced from other aggregators (reposted).

## Pitfalls

- **Many URL patterns** — images come from multiple CDN paths. Must filter carefully.
- **Thumbnails** use different paths (`/thumbs/`, `/antibandit/`) — don't confuse with full-size.
- **Biopic images** on the page may include thumbnails for _other_ celebs (sidebar/related). Download only images whose URL path contains the target celeb's slug.
- **No pagination** — single page per celeb.
