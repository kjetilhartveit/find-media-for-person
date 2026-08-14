---
name: find-media-from-fappeningbook
description: Use when you need to find and download media from Fappeningbook (fappeningbook.com) and TheFappeningBlog (thefappeningblog.com), both large aggregators with full-size images available.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for media of a specific person on Fappeningbook or TheFappeningBlog
- Extracting full-size images from thumbnails on Fappeningbook gallery pages
- Downloading image galleries from TheFappeningBlog (category pages and individual galleries)

# Find media from Fappeningbook / TheFappeningBlog

Two related aggregator sites with different image hosting patterns.

## URL Patterns

### Fappeningbook (fappeningbook.com)
- Profile: `https://fappeningbook.com/{slug}-nude/` — try person's name first (e.g. `caroline-nitter-nude/`), then their Instagram username if that 404s (e.g. `jessicah-o-nude/` for @jessicah_o), then try their OnlyFans/handle alias. The `us.fappeningbook.com` subdomain mirrors content.
- Image URLs: `https://fappeningbook.com/photos/{l1}/{l2}/{slug}/1000/{id}t.jpg` (thumbnail) → remove `t` for full-size (e.g. `1t.jpg` → `1.jpg`). Resolution segment is `1000`.

### TheFappeningBlog (thefappeningblog.com)
There are FOUR image patterns to extract:

**Pattern 1 — Gallery page (newer format, user-suggested):**
- Profile/gallery: `https://thefappeningblog.com/gallery/{slug}/` (e.g., `/gallery/inna/`)
- Paginated: `/gallery/{slug}/page-N/`
- Individual gallery: `/gallery/{slug}/{N}/` (gallery number) — each shows ONE full-size image
- Full-size images are inside `<a href="...">` tags in the article content

**Pattern 2 — Data directory (legacy format):**
- Gallery URLs: `https://thefappeningblog.com/gallery/{slug}/{N}/`
- Images: `https://thefappeningblog.com/data/{l1}/{l2}/{slug}/1000/{name}_{id}.jpg` (full-size)
- Thumbnail: `https://thefappeningblog.com/data/{l1}/{l2}/{slug}/1000/{name}_{id}_350px.jpg` (remove `_350px` for full-size)
- Slug is **lowercase** in URL (e.g., `/data/i/n/inna/1000/inna_0044.jpg`)
- When scraping listing pages, use case-insensitive regex for `Inna/inna/jpg`

**Pattern 3 — WordPress uploads (current format):**
- Images: `https://thefappeningblog.com/wp-content/uploads/YYYY/MM/name.jpg`
- Thumbnail: `https://thefappeningblog.com/wp-content/uploads/YYYY/MM/name_350px.jpg` (remove `_350px` for full-size)
- **Same thumbnail transformation as data directory: remove `_350px` suffix** to get full-size URL. No `_thefappeningblog.com_` suffix needed.
- Resized WordPress images have dimension suffixes like `-1024x576.jpg`, `-768x1024.jpg` — the actual full-size images do NOT have these dimension suffixes
- All images may be listed in a single page HTML when visiting the gallery page directly (no individual gallery sub-pages needed for WordPress uploads)
- Some WordPress images have embedded filename dimensions (e.g., `Inna-Sexy20--826x1024.jpg`) — these ARE the full-size version; WordPress may serve the same file for both full and resized URLs

**Pattern 4 — cnt directory (OnlyFans leaks):**
- Images at: `https://thefappeningblog.com/cnt/{l1}/{l2}/{slug}/{date-slug}/name.jpg`
- Format: `/cnt/m/e/{person-slug}/{YYYY-MM-DD-uuid}/{name}.jpg`
- Gallery URLs contain `megan-renee316-nude-onlyfans-leaks-` — these are NOT actual celebrity content, they are OnlyFans creator content misattributed.

**Gallery page structure:** Individual gallery pages show ONE full-size image per page. Gallery pages are numbered sequentially (1–N). The gallery listing page shows ALL galleries with thumbnails, numbered in reverse order (highest first). Gallery URLs may use different image formats (data directory vs. WordPress uploads).

**Finding galleries:** Use `https://thefappeningblog.com/gallery/{slug}/` first. If that fails, try web search: `site:thefappeningblog.com "person name"` and scrape category pages: `https://thefappeningblog.com/category/{slug}-2/page/{N}/`. Check up to 6-7 pages.

## Recommendations on how to download

### Fappeningbook
- Extract thumbnail URLs using the specific pattern `/photos/.../{id}t.jpg`. Avoid broad `*.jpg` grep which matches avatars and site assets.
- IDs are sequential per page (typically 1–26). Thumbnails appear in reverse order in HTML (highest ID first). Check for pagination links.
- Rate limiting: sleep 0.3–0.5s between requests.
- Validate downloaded files are > 10KB.

### TheFappeningBlog
- **Thumbnail transformation (unified):** For BOTH data directory and WordPress uploads, the full-size URL is obtained by simply removing `_350px` from the thumbnail URL: `name_350px.jpg` → `name.jpg`. This works with Python `.replace("_350px.jpg", ".jpg")`.
- **Listing page HTML structure:** Uses `<div class="item_content">` → `<a href=".../gallery/{slug}/{N}/">` → `<div class="item_img">` → `<img src="THUMBNAIL">`. Extract gallery number from href and thumbnail from img src.
- **Gallery pages:** Each individual gallery page shows ONE full-size image in `<a href="...jpg">`. Useful for verification or when listing pages are insufficient.
- **cnt/ directory (OnlyFans):** Only extract if you explicitly want OnlyFans leak content of the person.
- **Scraping:** For listing pages, extract thumbnails and apply the unified `_350px` → `.jpg` transformation. For individual gallery pages, extract from `<a>` tag in content area.
- Rate limiting: sleep 0.3–0.5s between requests.
- For large galleries: the full HTML may contain hundreds of images (WordPress embeds them all). Some sites use lazy loading — check `data-src` and `data-srcset` attributes.

## Quality

- **Fappeningbook images:** ~35KB–700KB (varies by content), 1000px wide thumbnails → full-size available at same URL minus `t`
- **TheFappeningBlog images (WordPress):** Full-size images typically 1100–1920px wide, ranging from ~80KB to 700KB+ depending on content
- **TheFappeningBlog images (data/):** Full-size ~800–1000px wide, ~35–230KB
- Some WordPress images have embedded dimensions in filename (e.g., `-820x1024`) — these ARE the original saved size, not WordPress-resized
- Generally good quality for an aggregator site

## Pitfalls

- **Some gallery pages are 404:** Gallery numbers may not be consecutive (e.g., galleries 36, 41 can be 404). Skip them gracefully.
- **No profile pages on fappeningbook.com for some celeb:** If `<name>-nude/` returns 404, try using `theappeningblog.com` instead. Fappeningbook.com profiles are for "OnlyFans creators" not celebrities.
- **fappeningbook.com search doesn't work well:** `/?s=query` returns 200 but no useful results — prefer direct URLs.
- **TheFappeningBlog category slug varies:** Try `-2`, `-3`, `-4` suffixes. Some use just the person's name, others have variations.
- **Web search is the best way to find TheFappeningBlog galleries:** Use `site:thefappeningblog.com "person name"` to discover relevant galleries.
- **OnlyFans leak galleries misclassified:** Some galleries labeled as a celebrity's "OnlyFans leaks" are actually from different creators. Check if the gallery URL contains names like `renee316` — skip these unless you want OnlyFans creator content.
- **No videos on fappeningbook.com profiles** — only static images. TheFappeningBlog may occasionally host videos.