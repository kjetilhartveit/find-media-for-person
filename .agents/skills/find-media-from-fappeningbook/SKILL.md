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
- Profile: `https://fappeningbook.com/{slug}-nude/` — try person's name first (e.g. `caroline-nitter-nude/`), then their Instagram username if that 404s (e.g. `jessicah-o-nude/` for @jessicah_o). The `us.fappeningbook.com` subdomain mirrors content.
- Image URLs: `https://fappeningbook.com/photos/{l1}/{l2}/{slug}/1000/{id}t.jpg` (thumbnail) → remove `t` for full-size (e.g. `1t.jpg` → `1.jpg`). Resolution segment is `1000`.

### TheFappeningBlog (thefappeningblog.com)
There are THREE image patterns to extract:

**Pattern 1 — Data directory (legacy format):**
- Category page: `https://thefappeningblog.com/category/{person-slug}-2/` (the `-2` is a WordPress category suffix; try variations like `-3`, `-4`)
- Gallery URLs: `https://thefappeningblog.com/{gallery-title}/` — slug often `megan-thee-stallion-{event}-{N}-photos`
- Images: `https://thefappeningblog.com/data/{l1}/{l2}/{slug}/1000/{name}_{id}_350px.jpg` → remove `_350px` for full-size

**Pattern 2 — WordPress uploads (current format):**
- Images: `https://thefappeningblog.com/wp-content/uploads/YYYY/MM/name_thefappeningblog.com_.jpg`
- Full-size images end with `_thefappeningblog.com_.jpg` (no dimension suffix like `-1024x1280`)
- Resized versions have `-1024x1280.jpg`, `-768x960.jpg`, `-240x300.jpg`, etc. — skip these
- All images are listed in a single page HTML (no URL pagination)

**Pattern 3 — cnt directory (OnlyFans leaks):**
- Images at: `https://thefappeningblog.com/cnt/{l1}/{l2}/{slug}/{date-slug}/name.jpg`
- Format: `/cnt/m/e/{person-slug}/{YYYY-MM-DD-uuid}/{name}.jpg`
- Gallery URLs contain `megan-renee316-nude-onlyfans-leaks-` — these are NOT actual celebrity content, they are OnlyFans creator content misattributed.

**Finding galleries:** Use web search to find category pages for a specific person, then scrape all pages: `https://thefappeningblog.com/category/{slug}-2/page/{N}/`. Check up to 6-7 pages.

## Recommendations on how to download

### Fappeningbook
- Extract thumbnail URLs using the specific pattern `/photos/.../{id}t.jpg`. Avoid broad `*.jpg` grep which matches avatars and site assets.
- IDs are sequential per page (typically 1–26). Thumbnails appear in reverse order in HTML (highest ID first). Check for pagination links.
- Rate limiting: sleep 0.3–0.5s between requests.
- Validate downloaded files are > 10KB.

### TheFappeningBlog
- **WordPress uploads:** Extract images matching `*_thefappeningblog.com_.jpg` (the full-size version). Filter out resized versions (with `-1024x`, `-768x`, `-240x`, `-624x`, `-1229x` etc.)
- **Data directory:** Extract images matching `/data/.../1000/..._350px.jpg`, remove `_350px` for full-size.
- **cnt/ directory (OnlyFans):** Only extract if you explicitly want OnlyFans leak content of the person.
- Rate limiting: sleep 0.3–0.5s between requests.
- For large galleries: the full HTML may contain hundreds of images (WordPress embeds them all). Some sites use lazy loading — check `data-src` and `data-srcset` attributes.

## Quality

- **Fappeningbook images:** ~45KB–111KB (themed), full-size ~1000px wide
- **TheFappeningBlog images (WordPress):** Full-size images typically 1100–1920px wide, ranging from ~80KB to 500KB+ depending on content
- **TheFappeningBlog images (data/):** Full-size ~1000px wide, ~50–150KB
- Generally good quality for an aggregator site

## Pitfalls

- **No profile pages on fappeningbook.com for some celeb:** If `<name>-nude/` returns 404, try using `theappeningblog.com` instead. Fappeningbook.com profiles are for "OnlyFans creators" not celebrities.
- **fappeningbook.com search doesn't work well:** `/?s=query` returns 200 but no useful results — prefer direct URLs.
- **TheFappeningBlog category slug varies:** Try `-2`, `-3`, `-4` suffixes. Some use just the person's name, others have variations.
- **Web search is the best way to find TheFappeningBlog galleries:** Use `site:thefappeningblog.com "person name"` to discover relevant galleries.
- **OnlyFans leak galleries misclassified:** Some galleries labeled as a celebrity's "OnlyFans leaks" are actually from different creators. Check if the gallery URL contains names like `renee316` — skip these unless you want OnlyFans creator content.
- **gallery/{slug} does not work for celeb galleries:** Individual gallery posts use the format `megan-thee-stallion-{descriptive-title}-{n}-photos/`
- **No videos on fappeningbook.com profiles** — only static images. TheFappeningBlog may occasionally host videos.