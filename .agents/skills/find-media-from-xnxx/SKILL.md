---
name: find-media-from-xnxx
description: Use when you need to find and download media from XNXX (xnxx.com), a pornographic video sharing website.
---

## Main website

- Website URL: https://www.xnxx.com/

## Search URLs

- Search by query: `https://www.xnxx.com/search/{query}/{page}`
  - Example: `https://www.xnxx.com/search/joon-mali/1`
  - Replace `{query}` with URL-encoded search terms and `{page}` with page number (1-based)

## Video URLs

- Individual video: `https://www.xnxx.com/video-{id}/{slug}`
  - Example: `https://www.xnxx.com/video-1adt33b1/sexy_busty_babe_joon_mali_posed_and_played_with_her_wet_pussy`

## Pornstar profile pages

- Pattern: `https://www.xnxx.com/pornstar/{slug}` — these often 404 even for performers with lots of content (slug variants like `{first}_{last}` also 404). Don't rely on them; use the site search instead.

## Posters / thumbnails without fetching every video page

- Search result pages embed all needed metadata per result, so no need to visit each video page:
  ```html
  <div id="video_{eid}" data-id="{numericId}" ...>
    ... data-src="https://thumb-cdnNN.xnxx-cdn.com/{uuid}/0/xn_N_t.jpg"     <!-- 600x337 thumb -->
        data-mzl="https://thumb-cdnNN.xnxx-cdn.com/{uuid}/0/mozaique_listing.jpg"  <!-- 960x540 -->
        data-pvv="https://thumb-cdnNN.xnxx-cdn.com/{uuid}/0/preview.mp4"    <!-- short preview clip -->
    <a href="/video-{eid}/{slug}" title="...">
  ```
- For downloading video posters, `mozaique_listing.jpg` (960x540, multi-frame mosaic) is the best available quality. Fall back to the `xn_N_t.jpg` thumb (600x337) if missing.
- Video pages' `og:image` is only the 600x337 thumb; larger in-page previews are loaded via JS and are not directly reachable with curl.

## Downloading with yt-dlp

XNXX supports HLS streaming. Use the following yt-dlp options:

```bash
yt-dlp -f "hls-1080p" \
  --merge-output-format mp4 \
  --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  "https://www.xnxx.com/video-{id}/{slug}"
```

**Important notes:**

- Use `-f "hls-1080p"` to get the best quality (1080p). Do NOT use `bestvideo+bestaudio` as this fails with XNXX.
- Always set a browser `--user-agent` to avoid 404 errors.
- Videos are served as HLS m3u8 streams in MP4 format.
- Available formats: `hls-250p`, `hls-360p`, `hls-480p`, `hls-720p`, `hls-1080p`
- Each 1080p video is typically ~115-120MB.

## Scraping tips

- Use `curl` to fetch search result pages and grep for video links:
  ```bash
  curl -s -L -A "Mozilla/5.0" "https://www.xnxx.com/search/{query}/{page}" | \
    grep -oP 'href="(\/video[^"]+)"' | sed 's/href="//;s/"$//' | sort -u
  ```
- Search results may contain videos of people with similar names. Filter manually by checking if the title contains the target person's name.
- Pagination: search URLs are paginated with `/1`, `/2`, `/3` etc. The last page number appears in the footer. Relevance degrades with page depth — deep pages return only generic keyword matches (e.g. searching "lela star" eventually returns "Luna Star", "Sara Star", "Star Wars", unrelated performers). Scan pages in batches and stop when the target name in titles stops appearing.
- The `/video-streams/{query}` URL pattern returns "Not found" - use `/search/{query}/` instead.
- Common surnames in search results: Search terms like "Fernandes" may return videos of unrelated performers (e.g., many Brazilian models named "Fernandes"). Always verify by checking titles or extracting video URLs and comparing against known results.
- Some models may not have videos on XNXX even if they appear on other sites (e.g., XHamster). If the search returns no matches for the person's name, they may not have content on XNXX.
- Spam re-uploads: the same scene often appears as many video IDs with paraphrased titles (e.g. "(name) scene in office clip-19/23/24..."), sometimes from upload farms (`/gift` promo titles, `THUMBNUM` slugs). Video titles cannot always be trusted for identity. Deduplicate by downloading posters and hashing the images; note re-uploads can have different thumbnail frames, so image-hash dedupe (not URL dedupe) is the reliable method.
- Video pages fetched with curl do not include a reliable cast/performer list, so identity can usually only be verified via the title/tags.
