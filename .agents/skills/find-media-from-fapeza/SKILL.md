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
- Page title may contain alternate names: `Linda Lan / foodsandnood.s / lindarainbow Nude Leaks OnlyFans - Fapeza` or `Jenaveve / Jenaveve Joli / Jenaveve Jolie / Jeneveve Jolie / Jenevieve / Jolie / Olivia / https: / jenaveve.jolie.official / jenavevejolie69 Nude Leaks OnlyFans - Fapeza`. Try alternate names as additional slugs to check for more content.
- **Note:** Some models never appear on Fapeza (e.g., Joon Mali — profile returned 404 on all slugs tried, site search returned 0 results in August 2026). Always verify by searching the site first (`fapeza.com/search?q=NAME`) before assuming a profile exists.
- Multiple profile slugs can exist for the same person under different aliases (e.g., "Megan" appeared as both `megan` and `megan-thee-stallion-1`).
- **Multiple slugs may have DIFFERENT content, not just duplicates:** (e.g., Collien Fernandes has both `collien-fernandes` with 6 posts and `collien-ulmen-fernandes` with 19 posts — different images on each, not overlapping). Kylie Jenner has both `kylie-jenner` (785 images, IDs 29-5826 with gaps) and `kyliejenner` (6 images, IDs 2-18) — distinct images, no overlap. Jenaveve Jolie has both `jenaveve-jolie` (19 posts, IDs 116-162) and `jenavevejolie69` (14 posts, IDs 1-16) — distinct images, no overlap. Always check all discovered slugs and combine unique images.
- **Important:** Always use the non-www domain (`fapeza.com`). The `www.` domain triggers a Cloudflare JS challenge (returns 401).
- Country-specific TLDs also exist: `cz.fapeza.com`, `de.fapeza.com`, `es.fapeza.com`, `fr.fapeza.com`, etc. (Found: cz, de, es, fr, gr, hu, it, jp, nl, pl, pt, ro, ru, se, tr, cn, in, kr, ua, eg, vn, th, bg, dk, rs, sk). These are mirrors.
- Profile slug may not match the exact display name. Try variations: full name, shortened name, underscore vs hyphen.
  - **Name ending in "Jenner":** Use no-hyphen slug (e.g., `laylajenner` works, but `layla-jenner` returns 404). Try the no-hyphen version first if the hyphenated version fails.

## Direct image URL pattern (bypass post pages)

- Direct image URLs can be constructed without visiting individual post pages:
  `https://fapeza.com/media/k/y/{slug}/{folder}/{filename}`
  - `folder = floor(post_id/1000)*1000 + 1000` (e.g., ID 1011→folder 2000, ID 5826→folder 6000, ID 29→folder 1000)
  - `filename`: For IDs >= 1000 → `{slug}_{id}.jpg` (e.g., `kylie-jenner_1011.jpg`); For IDs < 1000 → `{slug}_0{id}.jpg` or `{slug}_00{id}.jpg` (zero-padded to 4 digits, e.g., `kylie-jenner_0029.jpg`)
  - **Note:** The Referer header is NOT required for direct image URL requests.
  - This avoids the need to enumerate post IDs — you can attempt downloads directly and skip 404s.

## Recommendations on how to download

- Fapeza has sequential post IDs. URLs are predictable: base URL + ID-based paths.
- Full-size HQ images are available directly.
- Rate limiting: sleep 0.15–0.5s between requests. Cloudscraper sessions can be reused.
- Directory formula: `floor(id/1000)*1000 + 1000` for organizing downloads.

## Quality

- Images range from ~11KB (cover/thumbnail) to ~760KB per image.
- All verified downloads are JPEG format.
- First few posts (low IDs) may have smaller image sizes; subsequent posts have full HQ images.
- No videos have been found on Fapeza profiles (image-only content).

## Pagination

- Profile pages use `https://fapeza.com/{slug}/page-N/` for pagination, but **pagination is often non-functional** — pages either return 404, return the same content as page 1 (cycling), or show the same post IDs.
- Page 1 (no `/page-N/`) shows the posts for the profile.
- Use cloudscraper to check pages 2 and 3; if they return 404 or same post IDs as page 1, pagination is broken and you can stop.
- If pagination works, each page shows ~20 images.
- Profile pages typically show the ~20 most recent posts; older posts require checking by post ID.
- **Small profiles may have very few posts** (1-20). In such cases, all images are on page 1. Use the post ID range to determine if there might be more posts at higher IDs (check ID 100+ to see if it returns 404).

## Individual post URLs

- Individual post pages: `https://fapeza.com/{slug}/{post_id}/`
- Post IDs are sequential (e.g., `kate-hudson/1002/`, `kate-hudson/1001/`, `kate-hudson/1000/`, etc.)
- Individual post pages have **2 images each**: a common cover/ref image (shared across all posts in a profile) + the post-specific image. The shared image filename varies per profile (e.g., `_0006.jpg`, `_0012.jpg`, `_0016.jpg`). Consider skipping the shared cover to avoid duplicates.
- On **individual post pages**, images are already full-size (no `_400px.` suffix) — the thumbnail conversion is only needed on profile/gallery pages.
- **Filename padding:** All post images use 4-digit zero-padded filenames: `{slug}_{ID:04d}.jpg` regardless of ID value (e.g., `melissa-stratton-5_0001.jpg`, `melissa-stratton-5_0115.jpg`). Both low and high IDs follow the same 4-digit padding.
- **Dedup strategy on post pages:** The shared cover (e.g., `_0002.jpg` for `melissa-stratton-5`) appears on every post page. Skip it — the post-specific image can be identified as the one NOT matching the shared cover pattern.
- Profile pages may show ~1-20 images depending on profile size; smaller profiles (like Collien Fernandes with 6-19 posts) appear as a single page.
- **Post ID gaps can be very sparse:** Some profiles have high gap rates (e.g., 67% of IDs 1-115 were empty on one profile — only 77 of 115 IDs existed). When using direct URL pattern to download, expect many 404s and skip them. Do NOT assume contiguous ranges.

## Pitfalls

- Not all IDs exist — gaps in the lower ranges (below 5000). Only certain ID ranges have content.
- The Referer header is mandatory; omitting it will cause all image requests to fail.
- Image URLs in the page source are thumbnail URLs with `_400px.` suffix — remove `_400px.` to get the full-size image.
- Some posts (e.g., id 22) may live in a different folder (e.g., `1000`) than the recent ones (`2000`). Always use the direct URL from the page source.
- cloudscraper works reliably; no bot protection issues encountered.
- **Post ID 1000 on profile pages contains "related/recommended posts" from OTHER creators**, not profile content. When collecting images from profile pages, filter to only keep images with the profile's slug prefix (e.g., `megan_0021.jpg` not `jennierubyjane_0164.jpg`).
- Some models simply do not have content on Fapeza. For example, "Megan Vale" search returned 0 results. Always verify by searching the site first (`fapeza.com/search/?s=NAME`) before assuming a profile won't exist.
- Some individual post pages have only 1 image instead of the typical 2 (e.g., posts 38, 449, 453).
- Similar-looking slugs may be different people (e.g., "megan-stallion" vs "megan-thee-stallion-1") — verify by checking the page title before downloading.
- On profile pages, post links include full URLs: `<a href="https://fapeza.com/{slug}/{post_id}/">`. Extract the slug from these full URLs when building download paths.
- **Post ID ranges are sparse:** Never assume IDs 1-N are all populated. Always scan the range and filter 404s. Direct URL construction with 404 skipping is the most reliable method — no need to enumerate all valid IDs first.

## Typical stats

- Profile pages contain ~20 images (may be fewer for smaller profiles). Jenaveve Jolie main profile had 19 images; secondary profile had 14 images.
- Total images per profile varies widely (e.g., Kate Hudson: 72 images, ~12MB total; Linda Lan: 17 images, ~2.6MB total; Eleonora Bertoli: 67 posts, 68 unique images, ~12MB total; Melissa Stratton: 77 images, ~18MB total). Jenaveve Jolie profiles total ~33 images, ~6MB.
- Some models may have MULTIPLE profiles with different content (e.g., Kylie Jenner: `kylie-jenner` with 785 images ~121MB, and `kyliejenner` with 6 images). Jenaveve Jolie has `jenaveve-jolie` (19 images, ~2.3MB) and `jenavevejolie69` (14 images, ~4.0MB).
- Image files range from ~11KB (cover) to ~760KB. Profile content ranges from hundreds of KB to over 100MB.
- Post ID gaps can be very sparse — up to 67% of IDs in a range may not exist.
- All verified downloads are JPEG format.
- No videos have been found on Fapeza profiles (image-only content).
</think>

## Tips on changing photos to high quality in the browser

- Helper Script for Changing Photos to High Quality in the Gallery (in the browser). Use if needed:
  ```javascript
  document.querySelectorAll(".posts-wrapper img").forEach((img) => {
    img.src = img.src.replace(/_400px\.(\w+)$/, ".$1");
  });
  ```
