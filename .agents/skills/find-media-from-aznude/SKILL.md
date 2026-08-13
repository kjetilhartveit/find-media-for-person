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
- Celebrity page: `https://www.aznude.com/view/celeb/{initial}/{slug}.html` — first letter + lowercase slug
- Story pages: `https://www.aznude.com/view/story/{initial}/{slug}{story-description}.html`
- Images from CDN: `cdn2.aznude.com/{slug}/{category}/{filename}.jpg`
- User uploads (full-size): `user-uploads.aznude.com/data/azncdn/{hash}/{name}.jpg`
- Video thumbnails: `cdn2.aznude.com/antibandit/{slug}/{category}/thumb3_{name}.jpg`

## Recommendations on how to download

- **Slug variations** — try lowercase concatenated words (e.g., `megantheestallion`) and hyphenated (e.g., `megan-thee-stallion`). Not all celebs have a page — some will 404.
- **Stories** — celeb pages have story links loaded via JS. Extract story URLs with: `curl | grep -o 'href="/view/story/m/[a-z0-9-]*\.html'`. Then fetch each story URL to get its images from `user-uploads.aznude.com/data/azncdn/`.
- **Extract media URLs** using `curl | grep`:
  - Download full-size images from `user-uploads.aznude.com/data/azncdn/` paths (not `data/thumbs/`).
  - Download `cdn2.aznude.com/{slug}/` images (not `/antibandit/` thumbnails).
  - Filter out `/images/categories/` (category icons), `/sparkthumbs/`, and biopic images of unrelated celebs.
- **No auth required.** Rate limit: sleep 0.3–0.5s between requests.
- Some celeb pages may have 404 if no content exists — try slug variations.

## Quality

- Images: ~100KB–3MB for CDN images, ~150KB–300KB for user-upload images. User uploads tend to be higher quality.
- Content: mix of leaked photos, bikini/swimwear, scene stills from movies/TV, red carpet, and social media.
- Moderate value per celeb. Content may be sourced from other aggregators (reposted).

## Pitfalls

- **Slug format** — the slug may not follow simple hyphenation rules. Try both `slug` and `slug-name` variations.
- **Many URL patterns** — images come from multiple CDN paths. Must filter carefully.
- **Thumbnails** use different paths (`/thumbs/`, `/antibandit/`) — don't confuse with full-size.
- **Biopic images** on the page may include thumbnails for _other_ celebs (sidebar/related). Download only images whose URL path contains the target celeb's slug.
- **Stories loaded via JS** — story links on the celeb page are rendered client-side. Use curl/grep to discover story URLs, then process each individually.