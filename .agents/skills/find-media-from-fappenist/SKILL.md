# Skill: find-media-from-fappenist

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for media of a specific person on Fappenist (fappenist.com)
- Extracting full-size images from gallery pages and gallery view
- Similar to fappeningbook/fappeningblog but with different URL patterns

# Find media from Fappenist

## URL Patterns

### Gallery page (main content with pagination):
- URL: `https://www.fappenist.com/fappening/photos/{postId}/{slug}/`
- Paginated: append `?page=N` (0-indexed)
- Example: `https://www.fappenist.com/fappening/photos/26048/eleonora-bertoli-nude-and-sexy-collection`
- Page 0 is the base URL, page 1 is `?page=1`, etc.
- Each page typically shows 10 images
- Pagination link text: "Next page ( N of M )" where M is total pages

### Gallery view (all images in one page):
- URL: `https://www.fappenist.com/gallery/{postId}`
- Returns all images from the gallery in a single HTML page (masonry/grid layout)
- More efficient than paginated gallery pages
- Images are in `<figure>` elements with `<a>` tags pointing to full-size images

### Tag page (all posts for a person):
- URL: `https://www.fappenist.com/tag/{person-name}`
- Lists all posts/galleries for a person
- Example: `https://www.fappenist.com/tag/eleonora-bertoli`
- Usually one entry per gallery post with a link to the full gallery

### Category pages:
- URL: `https://www.fappenist.com/fappening/{category-name}`
- Browse by category (paparazzi, nude-sex-scene, nip-slip, etc.)

## Image URL Patterns

### Full-size images:
- URL: `https://www.fappenist.com/Uploads/Media/{Month}{Year}/{DayAbbrev}{DayNum}/{postId}/{hash}.jpg`
- Example: `https://www.fappenist.com/Uploads/Media/Jul24/Mon15/26048/6c553ff6.jpg`
- These are the actual images (no dimension suffix), typically 800px wide
- In gallery view `<a href="...">` tags give full-size image URLs

### Thumbnail images:
- URL: `https://www.fappenist.com/Uploads/Media/{Month}{Year}/{DayAbbrev}{DayNum}/{postId}/m_{hash}.jpg`
- Prefixed with `m_` (e.g., `/Uploads/Media/Jul24/Mon15/26048/m_6c553ff6.jpg`)
- Lower resolution versions used on listing pages

### HTML structure notes:
- Images are protocol-relative: `//www.fappenist.com/Uploads/...`
- Images in gallery view have `data-size="WxH"` attributes
- Gallery view figure elements: `<figure data-height="{H}" data-width="{W}">`
- No resized versions (like `-1024x768`) — the files shown are the original uploads

## Recommendations on how to download

### Site access:
- **Cloudflare Bot Management protection**: The site returns Cloudflare managed challenge (403) to curl/wget. Use `webfetch` which bypasses Cloudflare, or curl with proper User-Agent header.
- `gallery-dl` does NOT support fappenist — use web scraping with webfetch/curl.
- The `webfetch` tool successfully bypasses Cloudflare challenges and returns full HTML.

### From gallery view (recommended):
1. Navigate to `https://www.fappenist.com/gallery/{postId}`
2. Extract full-size image URLs from `<a href="...jpg">` tags in `<figure>` elements
3. The href attribute gives the full-size image URL directly (no suffix removal needed)
4. Download images using curl with proper User-Agent
5. Rate limit: 0.3-0.5s between downloads

### From paginated gallery pages:
1. Fetch each page: `?page=0`, `?page=1`, etc.
2. Extract image `src` or `data-src` attributes from `<img>` elements in `<article>` tags
3. These are full-size images (same format, no suffix)
4. Pagination link class: `gallery-mode`, shows page count like "Next page ( 1 of 4 )"

### From tag page:
1. Extract links to individual gallery posts from `<article>` elements
2. Each post has a `<a class="title">` link to the full gallery page

## Quality

- Full-size images are original uploads, typically 800px wide with varying heights (669–1075px common)
- No server-side resizing with dimension suffixes — the files are already the originals
- Images are served as progressive JPEGs, quality 80%
- Typical file size: 50KB–250KB depending on content
- Good quality for an aggregator site

## Pitfalls

- **Cloudflare protection**: Standard curl/wget returns 403 Cloudflare challenge. Must use `webfetch` or pass a proper browser User-Agent to curl.
- **No gallery-dl support**: Fappenist is not in gallery-dl's extractor list. Must use manual scraping.
- **Protocol-relative URLs**: Image URLs start with `//www.fappenist.com/` — prepend `https:` when fetching.
- **Images are already full-size**: Unlike some aggregator sites, fappenist doesn't serve resized versions with dimension suffixes. The images in the HTML are already the original uploads.
- **One gallery per collection**: Each gallery page is a single collection of images (typically 30-40 images).
- **Tag page is the best discovery method**: Use `https://www.fappenist.com/tag/{person-name}` to find all galleries for a person.