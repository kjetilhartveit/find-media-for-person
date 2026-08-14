---
name: find-media-from-fapeza
description: Use when you need to find and download media from Fapeza, an aggregator of leaked celebrity content with HQ images.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for HQ images of a specific celebrity/person on Fapeza
- Downloading images from a Fapeza profile page
- Scraping sequential IDs on a Fapeza profile

# Find media from Fapeza

Download images from Fapeza (https://fapeza.com), an aggregator site of leaked/nude celebrity content.

## URL Patterns

- Profile: `https://fapeza.com/{slug}/` (e.g., `fapeza.com/emily-ratajkowski/`)
- Media items follow sequential ID pattern
- Page title may contain alternate names: `Linda Lan / foodsandnood.s / lindarainbow Nude Leaks OnlyFans - Fapeza`. Try alternate names as additional slugs to check for more content.
- **Note:** Some models never appear on Fapeza (e.g., Joon Mali — profile returned 404 on all slugs tried, site search returned 0 results in August 2026). Always verify by searching the site first (`fapeza.com/search?q=NAME`) before assuming a profile exists.
- Multiple profile slugs can exist for the same person under different aliases (e.g., "Megan" appeared as both `megan` and `megan-thee-stallion-1`).
- **Multiple slugs may have DIFFERENT content, not just duplicates:** (e.g., Collien Fernandes has both `collien-fernandes` with 6 posts and `collien-ulmen-fernandes` with 19 posts — different images on each, not overlapping). Always check all discovered slugs and combine unique images.
- **Important:** Always use the non-www domain (`fapeza.com`). The `www.` domain triggers a Cloudflare JS challenge (returns 401).
- Country-specific TLDs also exist: `cz.fapeza.com`, `de.fapeza.com`, `es.fapeza.com`, `fr.fapeza.com`, etc.
- Profile slug may not match the exact display name. Try variations: full name, shortened name, underscore vs hyphen.

## Recommendations on how to download

- Fapeza has sequential post IDs. URLs are predictable: base URL + ID-based paths.
- Full-size HQ images are available directly.
- **Required:** Set a `Referer` header in requests. Without it, image requests return 404.
- Rate limiting: sleep 0.3–0.5s between requests is sufficient to avoid blocking.
- Directory formula: `floor(id/1000)*1000 + 1000` for organizing downloads.

## Quality

- Images range from ~42KB to ~520KB per image.
- All verified downloads are JPEG format.
- Good quality HQ images, consistent URL pattern.

## Pagination

- Profile pages use `https://fapeza.com/{slug}/page-N/` for pagination, but **pagination is often non-functional** — all pages return the same content.
- Page 1 (no `/page-N/`) shows the posts for the profile.
- Use cloudscraper to check multiple pages; if they all return the same set of post IDs, pagination is broken and you can stop.
- If pagination works, each page shows ~20 images.

## Individual post URLs

- Individual post pages: `https://fapeza.com/{slug}/{post_id}/`
- Post IDs are sequential (e.g., `kate-hudson/1002/`, `kate-hudson/1001/`, `kate-hudson/1000/`, etc.)
- Individual post pages have **2 images each**: a common cover/ref image (same for all posts in a profile, typically `_0016.jpg`) + the post-specific image. Only download the post-specific image (exclude `_0016.jpg`).
- On **individual post pages**, images are already full-size (no `_400px.` suffix) — the thumbnail conversion is only needed on profile/gallery pages.
- Profile pages may show ~1-20 images depending on profile size; smaller profiles (like Collien Fernandes with 6-19 posts) appear as a single page.
- Post IDs may have gaps (e.g., posts 2–21 present but 3, 4, 5, 6 missing).

## Pitfalls

- Not all IDs exist — gaps in the lower ranges (below 5000). Only certain ID ranges have content.
- The Referer header is mandatory; omitting it will cause all image requests to fail.
- Image URLs in the page source are thumbnail URLs with `_400px.` suffix — remove `_400px.` to get the full-size image.
- Some posts (e.g., id 22) may live in a different folder (e.g., `1000`) than the recent ones (`2000`). Always use the direct URL from the page source.
- cloudscraper works reliably; no bot protection issues encountered.
- **Post ID 1000 on profile pages contains "related/recommended posts" from OTHER creators**, not profile content. When collecting images from profile pages, filter to only keep images with the profile's slug prefix (e.g., `megan_0021.jpg` not `jennierubyjane_0164.jpg`).
- Some individual post pages have only 1 image instead of the typical 2 (e.g., posts 38, 449, 453).
- Similar-looking slugs may be different people (e.g., "megan-stallion" vs "megan-thee-stallion-1") — verify by checking the page title before downloading.
- On profile pages, post links include full URLs: `<a href="https://fapeza.com/{slug}/{post_id}/">`. Extract the slug from these full URLs when building download paths.

## Typical stats

- Profile pages contain ~20 images (may be fewer for smaller profiles).
- Total images per profile varies widely (e.g., Kate Hudson: 72 images, ~12MB total; Linda Lan: 17 images, ~2.6MB total).
- Image files range from ~16KB to ~520KB.
- Profile content ranges from hundreds of KB to several MB.
- All verified downloads are JPEG format.
</think>

## Tips on changing photos to high quality in the browser

- Helper Script for Changing Photos to High Quality in the Gallery (in the browser). Use if needed:
  ```javascript
  document.querySelectorAll(".posts-wrapper img").forEach((img) => {
    img.src = img.src.replace(/_400px\.(\w+)$/, ".$1");
  });
  ```
