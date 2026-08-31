# Skill: find-media-from-jjgirls

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Downloading image galleries from jjgirls.com (jjgirls) — a large adult photo gallery site
- Searching for models across multiple aliases in one gallery
- jjgirls aggregates content from various adult sites (teencoreclub, nubilesnet, spoiledvirgins, etc.)

# Main website

- Base URL: `https://jjgirls.com`
- Model gallery: `https://jjgirls.com/pornpics/{model_name}` (e.g., `jjgirls.com/pornpics/amber-hardin`)
- Gallery detail: `https://jjgirls.com/pornpics/{source}-{model_alias}-{gallery_name}`
- Tags/categories: `https://jjgirls.com/pornpics/` with category filters (big-tits, anal, lesbian, etc.)

## Example URLs

- Amber Hardin: `https://jjgirls.com/pornpics/amber-hardin`
- Vasilisa: `https://jjgirls.com/pornpics/vasilisa`
- Veronica: `https://jjgirls.com/pornpics/veronica`

# Gallery Structure

- Each model page shows 15-16 gallery thumbnails per page
- **Pagination adds new content** — pages 1, 2, 3+ show different gallery sets. Check all available pages.
- Each gallery contains 10-33 individual images
- Total: typically 16 galleries × 15-20 images per page × 2-3 pages = ~500-1000+ images total

## Image URL Pattern

```
https://x.jjj.cam/pics/{studio}/{model_alias}/gallery_name/hd-{model_alias}-{number}.jpg
```

Examples:
- `https://x.jjj.cam/pics/teencoreclub/amber-hardin/sexhd-young-imags/hd-amber-hardin-5.jpg`
- `https://x.jjj.cam/pics/nubilesnet/amber-hardin/fighthdsex-ass-tori-bugil/hd-amber-hardin-5.jpg`
- `https://x.jjj.cam/pics/femjoy/vasilisa-amber-hardin/mystery-solo-loboporno/hd-vasilisa-amber-hardin-13.jpg`

Common studios/sources:
- teencoreclub, nubilesnet, pickupfuck, femjoy, spoiledvirgins, smackmybitch, clubseventeen, teendreams, just18, atmarchives, metart, private, ifuckedherfinally, etc.

# Key findings from searches

- **jjgirls has aliases as cross-links**: The model page lists aliases that link to separate pages (e.g., amber-hardin page links to vasilisa, veronica, ksenia, polina pages)
- **Alias pages DON'T contain additional Amber Hardin content**: Pages for aliases like "veronica", "polina", "ksenia", "alanova" have no images tagged specifically with "amber-hardin"
- **Cross-alias appears in URLs**: Some URLs combine aliases like "vasilisa-amber-hardin" or "amber-hardin-oliver-strelly"
- **Image quality**: Full-size HD images (20-73 KB each, typically 480-720px), served as `hd-{name}.jpg`
- **gallery-dl NOT supported**: No jjgirls extractor found; manual scraping required

# How to download

## Method 1: Manual scraping (preferred, gallery-dl not supported)

1. **Fetch model page**: `curl -sL "https://jjgirls.com/pornpics/{model_name}" > model.html`
2. **Extract all gallery links**: Look for `href="/pornpics/{source}-{alias}-..."` patterns
3. **For each gallery, extract images**:
   - Fetch each gallery page: `curl -sL "https://jjgirls.com/pornpics/{gallery-slug}" > gallery.html`
   - Extract image `src` attributes containing the model alias: `grep -oP 'src="https?://x\.jjj\.cam/pics/[^"]*"' gallery.html`
   - Filter for images matching `*.jpg` and containing the model's alias pattern
4. **Download images**: Use `curl -sLO --max-time 15 -A "Mozilla/5.0" -o {prefixed_name} {image_url}`
   - **Always prefix filenames with gallery source to avoid collisions**
   - Add 0.3-0.5s delay between downloads
5. **Deduplicate**: Many galleries share the same numbered images (hd-amber-hardin-1.jpg in multiple galleries)

## Method 2: Using web scraper

```bash
# Get all gallery slug patterns
grep -oP 'href="/pornpics/[a-z]+-[a-z]+-{alias}[^"]*"' page.html | sed 's/href="//' | sed 's/"$//' | sort -u

# For each gallery, get image URLs
grep -oP 'src="https?://x\.jjj\.cam/pics/[^"]*\.jpg"' gallery.html | grep -oP 'https?://[^"]+' | sort -u
```

# Pitfalls

- **Pagination does add new galleries**: Pages 2, 3, 4+ of a model's gallery show DIFFERENT galleries with additional content. Always check multiple pages.
- **Gallery image filenames collide**: The same `hd-model-1.jpg` appears in many different galleries — **always use source/prefix naming**
- **Alias pages are mostly unrelated**: Checking alias pages (e.g., "veronica") may return many images but very few (often zero) are actually tagged with the target model's "amber-hardin" alias
- **Only download images tagged with the target alias**: Use `grep 'amber-hardin'` to filter relevant images from alias pages
- **Some galleries combine aliases in URL**: e.g., `nubilesnet/amber-hardin` and `femjoy/vasilisa-amber-hardin` — filter for images containing the primary alias
- **Gallery thumbnails ARE full-size images**: The thumbnail images on the main page are the actual HD images (not placeholders)
- **Rate limit to 0.5s between requests**: The site uses caching but aggressive scraping may trigger blocks
- **Images come from x.jjj.cam CDN**: Direct URL pattern — no need for Referer headers typically

# Known good aliases for searching

When searching across aliases (per shared-find-media-guidelines), prioritize:
- Primary name + known aliases (e.g., "amber-hardin", "vasilisa-amber-hardin")
- Russian-sounding names that match the model's origin
- Verify images actually contain the target person's alias in the URL path

# Gallery-to-source mapping examples

| Gallery Page Slug | Source Studio |
|---|---|
| `teencoreclub-amber-hardin-feetto-teen-pornharmony` | teen-core-club |
| `nubilesnet-amber-hardin-sxe-babe-eating` | NubilesNet |
| `pickupfuck-amber-hardin-mobileporno-cumshot-cybergirl` | Pickup Fuck |
| `femjoy-vasilisa-amber-hardin-pornimage-solo-siki` | FemJoy |
| `spoiledvirgins-amber-hardin-majority-groupsex-xdporner-mobile-xxximages` | Spoiled Virgins |
| `smackmybitch-amber-hardin-smart-anal-fuck-xxxgirl-ero-seximages` | SmackMyBitch |
| `clubseventeen-amber-hardin-show-big-tit-cumshot-liveporn-mobile-sex-photos` | Club 17 |
| `teendreams-amber-hardin-site-amateur-broken` | Teen Dreams |
| `just18-amber-hardin-fresh-anal-gateway-erotic-xxxpictures` | Just18 |

Base directory for this skill: /home/kjetil/_index/git/find-media-for-person/.agents/skills/find-media-from-jjgirls
Relative paths in this skill (e.g., scripts/, reference/) are relative to this base directory.
Note: file list is sampled.