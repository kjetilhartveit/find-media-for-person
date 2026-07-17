---
name: find-media-from-pictoa
description: Download high-quality media from Pictoa by scraping album pages for image URLs.
---

# Find media from Pictoa

Download images from Pictoa (https://www.pictoa.com), a gallery site with albums of celebrity content.

## URL Patterns

- Site: `https://www.pictoa.com`
- Albums found via search for celebrity name
- Thumbnail CDN: `t1.pictoa.com`
- High-quality CDN: `s2.pictoa.com`
- Example path of a thumbnail image: https://t1.pictoa.com/media/galleries/282/396/282396602d9948ac637/3926902602d994abc044.jpg
- Example path of a large/high quality image: https://s2.pictoa.com/media/galleries/282/396/282396602d9948ac637/3926902602d994abc044.jpg

## Recommendations on how to download

1. Search for the celebrity name to find relevant albums.
2. Fetch each album/gallery page to extract image URLs.
3. Replace `//t1.` with `//s2.` in thumbnail URLs to get high-quality versions from `s2.pictoa.com`.
4. Manual pagination needed — scrape each album page individually.
5. Rate limiting: sleep 0.3–0.5s between requests.

## Quality

- Images range from ~15KB to ~35KB (smaller than other sources).
- Good quality images but labor-intensive. Requires scraping each album page.

## Pitfalls

- **URLs must be extracted from album pages.** Cannot guess URL patterns — manual scraping required.
- Labor-intensive: one page fetch per album to extract all image URLs.
- Multiple albums may exist per celebrity — search results need to be paginated.
- File sizes are smaller than other aggregator sources.

## Tips on changing photos to high quality in the browser

- Script for Changing Photos to High Quality in the Gallery (in the browser). Use if needed:
  ```javascript
  $$(".wrapper img").forEach((img) => {
    if (img.src) img.src = img.src.replace("//t1.", "//s2.");
    if (img.dataset.src)
      img.dataset.src = img.dataset.src.replace("//t1.", "//s2.");
  });
  ```
