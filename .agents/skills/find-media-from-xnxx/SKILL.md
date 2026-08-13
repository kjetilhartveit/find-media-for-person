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
- Pagination: search URLs are paginated with `/1`, `/2`, `/3` etc. Stop when no results appear for a page.
- The `/video-streams/{query}` URL pattern returns "Not found" - use `/search/{query}/` instead.
