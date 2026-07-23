---
name: find-media-from-fapeza
description: Download media from Fapeza, an aggregator of leaked celebrity content with HQ images.
---

# Find media from Fapeza

Download images from Fapeza (https://fapeza.com), an aggregator site of leaked/nude celebrity content.

## URL Patterns

- Profile: `https://fapeza.com/{slug}/` (e.g., `fapeza.com/emily-ratajkowski/`)
- Media items follow sequential ID pattern

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

- Profile pages use `https://fapeza.com/{slug}/page-N/` for pagination (confirmed working up to page 30+).
- Page 1 (no `/page-N/`) shows the 20 most recent posts.
- Each pagination page shows ~20 images.
- Use cloudscraper to fetch each page sequentially until a page returns no new images or 404.

## Individual post URLs

- Individual post pages: `https://fapeza.com/{slug}/{post_id}/`
- Post IDs are sequential (e.g., `kate-hudson/1002/`, `kate-hudson/1001/`, `kate-hudson/1000/`, etc.)
- Individual POST pages may NOT contain image links — images are only on profile/gallery pages.

## Pitfalls

- Not all IDs exist — gaps in the lower ranges (below 5000). Only certain ID ranges have content.
- The Referer header is mandatory; omitting it will cause all image requests to fail.
- Image URLs in the page source are thumbnail URLs with `_400px.` suffix — remove `_400px.` to get the full-size image.
- Some posts (e.g., id 22) may live in a different folder (e.g., `1000`) than the recent ones (`2000`). Always use the direct URL from the page source.
- cloudscraper works reliably; no bot protection issues encountered.

## Typical stats

- Profile pages contain ~20 images per page.
- Total images per profile varies (e.g., Kate Hudson: 72 images, ~12MB total).
- Image files range from ~16KB to ~520KB.
- All verified downloads are JPEG format.

## Tips on changing photos to high quality in the browser

- Helper Script for Changing Photos to High Quality in the Gallery (in the browser). Use if needed:
  ```javascript
  document.querySelectorAll(".posts-wrapper img").forEach((img) => {
    img.src = img.src.replace(/_400px\.(\w+)$/, ".$1");
  });
  ```
