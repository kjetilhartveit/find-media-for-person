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
- A person can have MULTIPLE profiles (display name + each alias). Check every candidate slug and compare image ID ranges/quality to decide if sets are the same source.
- Beware name collisions: a profile for one of the person's aliases may belong to a DIFFERENT person (e.g. a current OF creator with the same name — the profile title often carries the target's handle, which is the identity signal). Verify alias content against the target's biography before downloading.
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
- Resized WordPress images have dimension suffixes like `-1024x576.jpg`, `-768x1024.jpg` — the base URL without a suffix is the originally uploaded file, **but it frequently returns 404** (original removed from the server while resized copies remain). Observed largest available variants: `-768x1152` (portrait content), `-1536x1536` (square), `-1024x683` (2:1 covers)
- **Recommended full-size strategy:** collect ALL sized variants of each image from the article HTML (they are all present in `srcset` attributes), try the no-suffix original first, and on 404 fall back to the largest-suffix variant by pixel width
- All images may be listed in a single page HTML when visiting the article/gallery page directly (no individual gallery sub-pages needed for WordPress uploads)
- Some WordPress images have embedded filename dimensions (e.g., `Inna-Sexy20--826x1024.jpg`) — these ARE the full-size version; WordPress may serve the same file for both full and resized URLs
- Article HTML also contains sidebar "related articles" images of OTHER people and ad assets (e.g. `/data/...`, `porndude.png`) — filter to image URLs containing the target person's name

**Pattern 4 — cnt directory (OnlyFans leaks):**
- Images at: `https://thefappeningblog.com/cnt/{l1}/{l2}/{slug}/{date-slug}/name.jpg`
- Format: `/cnt/m/e/{person-slug}/{YYYY-MM-DD-uuid}/{name}.jpg`
- Gallery URLs contain `megan-renee316-nude-onlyfans-leaks-` — these are NOT actual celebrity content, they are OnlyFans creator content misattributed.

**Gallery page structure:** Individual gallery pages show ONE full-size image per page plus sidebar images of OTHER people (usually `/data/...` URLs with a different slug — filter to URLs containing the target's name). Gallery pages are numbered sequentially (1–N), but gaps occur. The gallery listing page shows galleries with thumbnails, numbered in reverse order (highest first). Gallery URLs may use different image formats (data directory vs. WordPress uploads).
- **One person can have TWO gallery slugs:** the display name (`/gallery/{slug}/`) AND their social handle (e.g. `/gallery/andreaespadatv/`). The handle-slug gallery is often the adult-era/alias content (the title concatenates all known names: "Name / Alias1 / Alias2"). Check the handle slug too.
- **Gallery listing pagination loops:** `/gallery/{slug}/page-N/` may repeat page-1 content or return small overlapping pages. Dedupe by gallery number and stop when no NEW galleries appear in a page.
- **Galleries only cover PART of a collection:** for a "N Photos" article, individual galleries may exist for only some of the N photos. Always find the main article and extract its full image set (below).

**Finding galleries/articles:** Use `https://thefappeningblog.com/gallery/{slug}/` first. If that fails (404), use web search `site:thefappeningblog.com "person name"` and scrape category pages: `https://thefappeningblog.com/category/{slug}-2/page/{N}/`. Check up to 6-7 pages.
- Many porn stars/actresses have NO `/gallery/` page — their content lives in individual **articles** (e.g. `/{name}-nude-porn-collection-N-photos/`, `/{name}-{topic}-N-pics-video/`). Web search is the reliable way to find these.
- The `/category/{slug}/` page reliably links the main article(s) for a person (often the "N Photos" collection). Fetch it and extract ALL image URLs from the article HTML in one pass (filter to the target's name) — usually yields the complete set, including photos missing from the individual galleries.
- Tag pages exist (`/tag/{slug}-naked/`) and list some articles, but can be incomplete — always cross-check with web search, and scrape every article found for image URLs.

### Forum threads (TheFappeningBlog)
TheFappeningBlog has a **forum section** where users post image sets and linked galleries about celebrities. This is valuable when no gallery/category page exists for a person.
- Thread URL: `https://thefappeningblog.com/forum/threads/{slug}.{thread_id}/` (e.g., `/forum/threads/melissa-stratton.112003/`)
- Find threads via web search: `site:thefappeningblog.com/forum "person name"`
- Threads are paginated: `/forum/threads/{slug}.{thread_id}/page-{N}/`
- Images embedded as attachments use pattern: `https://thefappeningblog.com/forum/data/attachments/{dir}/{id}-{hash}.jpg` — these are **publicly accessible** without login
- Some forum attachments use `/forum/attachments/` URLs which **require login** to download (skipped if not available)
- To extract attachment images from forum pages, regex search for `/forum/data/attachments/\d+/\d+-[a-f0-9]+\.jpg` in the HTML
- The thread starter's posts often include external links (login-walled) and some uploaded attachments
- Users reply with "More." posts and external image links — these are also login-walled
- Downloaded forum attachment images are typically moderate quality (~200-350KB, resized for forum display)

## Recommendations on how to download

### Fappeningbook
- Extract full-size URLs from `data-orig` attributes in `<a>` tags: `data-orig="https://fappeningbook.com/photos/{l1}/{l2}/{slug}/1000/{id}.jpg"` (no `t` suffix = full-size). Also extract thumbnails from `src` attributes: `/photos/{l1}/{l2}/{slug}/1000/{id}t.jpg`. Avoid broad `*.jpg` grep which matches avatars and site assets.
- IDs are sequential per page. Thumbnails appear in reverse order in HTML (highest ID first). Page 1 typically has 50 images; additional pages follow. Image IDs are not always contiguous (some gaps).
- Pagination: Page 2+ URLs include a `#photos` anchor: `https://fappeningbook.com/{slug}-nude/{page}/#photos`. Look for `class="pages-dv"` in the HTML to find pagination links (e.g., `Previous`, `Next`, `Page X of Y`).
- **Many profiles have a single page:** the `pages-dv` div is EMPTY and page-2+ URLs just serve page-1 content again (HTTP 200). Stop immediately if page 2 yields 0 new image IDs — never auto-increment based on a bare "Next" string elsewhere in the HTML (causes infinite loops).
- Rate limiting: sleep 0.3–0.5s between requests.
- Validate downloaded files are > 10KB.

### TheFappeningBlog
- **Thumbnail transformation (unified):** For BOTH data directory and WordPress uploads, the full-size URL is obtained by simply removing `_350px` from the thumbnail URL: `name_350px.jpg` → `name.jpg`. This works with Python `.replace("_350px.jpg", ".jpg")`.
- **Listing page HTML structure:** Uses `<div class="item_content">` → `<a href=".../gallery/{slug}/{N}/">` → `<div class="item_img">` → `<img src="THUMBNAIL">`. Extract gallery number from href and thumbnail from img src.
- **Gallery pages:** Each individual gallery page shows ONE full-size image in `<a href="...jpg">`. Useful for verification or when listing pages are insufficient.
- **Forum threads:** Extract attachment images via regex `/forum/data/attachments/\d+/\d+-[a-f0-9]+\.jpg`. These are publicly accessible. Paginate through all pages. Some `/forum/attachments/` URLs require login (skip these).
- **cnt/ directory (OnlyFans):** Only extract if you explicitly want OnlyFans leak content of the person.
- **Scraping:** For listing pages, extract thumbnails and apply the unified `_350px` → `.jpg` transformation. For individual gallery pages, extract from `<a>` tag in content area.
- Rate limiting: sleep 0.3–0.5s between requests.
- For large galleries: the full HTML may contain hundreds of images (WordPress embeds them all). Some sites use lazy loading — check `data-src` and `data-srcset` attributes.

## Quality

- **Fappeningbook images:** ~35KB–700KB (varies by content), 1000px wide thumbnails → full-size available at same URL minus `t`
- **TheFappeningBlog images (WordPress):** Full-size images typically 1100–1920px wide, ranging from ~80KB to 700KB+ depending on content. When the original is gone, the largest sized variant is usually ~768px wide (portrait) / ~1536px (square)
- **TheFappeningBlog images (data/):** Full-size ~800–1000px wide, ~35–230KB
- **TheFappeningBlog forum attachments:** Moderate quality, typically ~25–35KB (forum-optimized), resized for display
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
- **Cross-site "dupes" don't hash-match:** Fappeningbook photo IDs and TFB "N Photos" article numbers are often the same source series, but served as different files (crop/quality differ), so md5 dedupe across the two sites finds nothing. Keep both sets; name files by origin prefix + source ID.
- **WordPress originals 404:** The no-suffix `/wp-content/uploads/` URL often returns 404 while its sized variants work — do not stop at one 404, fall back to the largest sized variant (see Pattern 3).
- **Missing images are permanently gone:** When an image is removed, all its variants 404 on the main domain AND mirror subdomains (`us.`, `ca.`, `the.`) — no need to retry mirrors repeatedly.
- **Forum threads may be empty of attachments:** A thread about a person can have 0 public attachments across all its pages — still worth checking, but don't expect results.
- **Video thumbnails:** Collection articles may include wide (`-768x502` etc.) images that are video thumbnails with `__thumb1.jpg` names in the HTML — these are the external video's cover, not a photo; skip unless you also want the video (videos are external/embedded, not hostable here).