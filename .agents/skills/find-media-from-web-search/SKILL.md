---
name: find-media-from-web-search
description: Use when you need to find media via Google Images and web search by discovering article URLs, then extracting image URLs efficiently.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for photos of a person via web search engines or Google Images
- Searching articles mentioning a person with specific queries (e.g. "bikini", "photos", "vacation")
- Find media of a person who's not a well-known celebrity with dedicated aggregator pages

# Find media via web search / Google Images

Use web search engines and Google Images to find articles, news posts, and galleries that contain photos of a person, then extract and download the actual images.

## General Workflow

1. **Search**: Use `web_search` to find articles mentioning the person + target query (e.g. name + "bikini", "photos", "vacation", "leaks" etc.). Try name variations (English, local language, handle, full name).
2. **Extract images**: For each article URL found, extract image URLs efficiently (see strategies below).
3. **Download**: Use `curl` to download images to the target directory.
4. **Report**: Track which articles yielded images, how many, and quality.

## Possible Image Extraction Strategies

### Strategy 1: `web_fetch` with markdown format (Recommended)

Fetch the article using `format: "markdown"` — this strips most HTML bloat and often retains image URLs inline. The output is small and fits in context easily. This is the fastest, least context-heavy approach.

```
web_fetch(url, format: "markdown")
```

Look for image URLs in the markdown — they appear as `![...](url)` or bare URLs.

### Strategy 2: `web_fetch` with text format fallback

If markdown doesn't yield images, try `format: "text"` to get plain text. Some pages embed image URLs in the text body.

### Strategy 3: `web_fetch` with HTML — extract only `<head>` meta tags

When you need to fetch HTML, first extract the `<head>` section only (or the first ~100 lines) to get og/twitter meta tags:

- `<meta property="og:image" content="URL">` — cover image
- `<meta name="twitter:image" content="URL">` — cover image
- `<meta property="og:image:width">` / `og:image:height` — dimensions

This gives you at least one high-quality image per article with minimal context impact (~2KB vs 50KB for full page).

### Strategy 4: `curl` + regex for HTML extraction

Instead of `web_fetch` (which consumes context for the full HTML), use `curl` piped to `grep`/`rg` to extract image URLs directly to stdout:

```bash
# Extract all image URLs from an article
curl -sL "$URL" | grep -oP 'https?://[^"'"'"'<>]+\.(jpg|jpeg|png|webp)(\?[^"'"'"']*)?' | grep -v 'placeholder\|logo\|icon\|favicon\|ad\|banner\|pixel'

# Extract og:image and twitter:image meta tags
curl -sL "$URL" | grep -oP '(og:image|twitter:image)["'"'"']*[^=]*=["'"'"']\K[^"'"'"']+'
```

This avoids filling the agent context with HTML. The image URLs appear in the tool output directly.

### Strategy 5: Full HTML via `web_fetch` (Last Resort)

Only read full HTML when strategies 1-4 fail. Sites have very different image patterns, here's a few examples:

- **allkpop.com**: Images in `<figure><img src="/upload/...">` — full URLs need the domain prepended (e.g. `https://www.allkpop.com/upload/2026/05/content/...`)
- **koreaboo.com**: WordPress site. Images have `data-orig="URL"` attribute for full-size. Regular `src` is resized. Use `data-orig` when available. CDN: `image.koreaboo.com`
- **kpopbreaking.com**: WordPress. Images in `<img src="https://kpopbreaking.com/wp-content/uploads/...">`
- **mk.co.kr**: Images from `wimg.mk.co.kr` CDN. Thumbnail suffix `_P1.jpg`, resize `_R.jpg`

## Avoiding Premature Agent Termination

Large JS-heavy websites (typical news sites) are 50-300KB of HTML full of ad scripts. Fetching these via `web_fetch` consumes most of an agent's context budget in a single call. To avoid this:

- **Prefer `curl | grep` over `web_fetch`** — keeps image URLs in tool output without flooding the context with HTML.
- **Fetch at most 2-3 articles per sub-agent** — 50KB HTML × 4 pages = 200KB, which can exhaust context.
- **Process articles sequentially, not in parallel** — after extracting images from one article, download them immediately and move on. Don't fetch 4 articles and then process.
- **Strip/crop HTML when possible** — if you must use `web_fetch` HTML format, grep the output for image patterns rather than letting the agent parse the full HTML mentally.
- **Set a clear per-article budget** — if an article's HTML is too large or yields no images, skip it and move to the next.

## Search Query Tips

- Include social media handles: `"<handle> bikini"`, `"@<handle> photos"`
- Target image-heavy sites in search.
- For explicit/deepfake content, try specific aggregator sites: `thotdeep.com`, `sexcelebrity.net`, `realdeepfakes.com`. stk.st does NOT have dedicated person pages — use search queries or try other sources instead.
- For deepfake content of musicians, use full legal names (e.g. "Tyla Laura Seethal") in combination with mononym ("Tyla").
- Search on adult tube sites using variations: tube queries may return content tagged under the person's legal name or mononym.
- **Search for aliases/handles**: Many creators use different names/handles across platforms (e.g., Instagram handle vs. display name vs. OnlyFans username). Search for content using the creator's social media handles, aliases, and known platform-specific usernames on aggregator sites. These handles often appear as image gallery slugs or tag names on aggregator sites.

## Deepfake / Adult Aggregator Site Notes

- **ThotDeep** (thotdeep.com): Dedicated deepfake porn site with celebrity categories. URLs for thumbnails (e.g. `cdn*.thotdeep.com/images/thotdeep/*/thumbnail.jpg`) often return HTML error pages instead of real images — always verify with `file` command. Profile images (e.g. `img-st*.thotdeep.com/*/player.jpg`) are usually real images. All content is AI-generated/fakeswap — not real footage.
- **SexCelebrity** (sexcelebrity.net): Search-based site for "person + creampie/deepfake". May return 504 errors.
- **RealDeepFakes** (realdeepfakes.com): Social platform for deepfake creators. Requires login for full access. Search has many results per celebrity.
- **stk.st** (stk.st): General celebrity adult content aggregator. NOTE: `stk.st/{person}` URLs do NOT show person-specific content — they show a generic gallery. Use `stk.st/search?query=person+leak` instead. Image URLs follow pattern: `https://i3.wp.com/{cdn}/{path}/{filename}.jpg`.
- **stk.st** images are served from multiple CDNs: `i3.wp.com`, `i0.wp.com`, `i2.wp.com`, `i1.wp.com` (WordPress.com CDN). The CDN host in the URL is variable.

## Celebrity Nude Photo Aggregators

These sites maintain dedicated galleries per celebrity and are high-value sources:

- **AZNude** (aznude.com): 80+ photos for major celebs. Celebrity pages at `/view/celeb/{initial}/{slug}-{id}.html`. Image URLs: `https://cdn2.aznude.com/{hash}/{hash}.jpg` for full-size (640px wide JPEG). Thumbnails have `thumb3_` prefix. Story pages (galleries within a celeb page) use JS rendering — `curl | grep` won't find images there. Extract from the main celebrity index page instead. Also has `/view/story/c/{slug}.html` story pages where full-size images are linked from markdown link format: `](https://user-uploads.aznude.com/data/azncdn/{slug}/{hash}/{imageId}.jpg)`.
- **CelebGate** (celeb.gate.cc): Dedicated celebrity nude photo gallery site. Gallery at `/{slug}/gallery.html`. Image URLs: `http://celeb.gate.cc/media/cache/image/upload/{initial}/y/{slug}-{id}.jpg` (use `data-orig` attribute for full-size, replace `http` with `https`). Verify image validity by checking file size > 100 bytes. Some CelebGate pages redirect HTTP to HTTPS (301).
- **CelebHub** (celebhub.net): Similar format. Celebrity page at `/celebrity/{slug}`.
- **Babepedia** (babepedia.com): Profile pages with user-uploaded photos. Images at `/pics/{Slug}.jpg` (main), `/pics/{Slug}N.jpg` (additional). Also has `/user-uploads/` directory for community uploads. Useful for aliases/biographical data.
- **ModelsIntro** (modelsintro.com): Professional model photo gallery with 100-600+ photos per model. Uses JavaScript-rendered image URLs with token-based auth (`/gallery/loadimage.php?token=...`). Image extraction requires `web_fetch` markdown format — images appear as `![](/gallery/loadimage.php?token=...)`. Pagination via `/page/{n}`. Each photo link includes width/height params for thumbnails. Full-size images need larger token requests.
- **Pictoa** (pictoa.com): Adult photo album site. Album URLs: `/albums/{slug}-{id}.html`. Images at `https://t1.pictoa.com/media/galleries/{hash}/{album_id}{timestamp_hex}.jpg`. Album IDs contain a hex timestamp suffix. Multiple albums per celeb may exist.
- **EroMe** (erome.com): User-hosted adult content sharing with albums. Album URLs: `https://erome.com/a/{albumId}`. Extract full-size image URLs by searching the HTML for `https://s{N}.erome.com/{id}/{albumId}/thumbs/{imgId}.jpg` and removing `/thumbs/` to get the full-size URL pattern `https://s{N}.erome.com/{id}/{albumId}/{imgId}.jpg`. Albums may contain many images across multiple server subdomains (s2, s10, s15, s19, s20, s22, s3, s41-s83, etc.). Use `curl | grep -oE` to extract thumbnail URLs, then `sed 's|/thumbs/|/|g'` to get full-size. Some albums have 50-100+ images. EroMe content is often tagged with the creator's alternate handles, aliases, or display names — search for content using multiple name variations.

## Fashion/Reveal Article Sources

These sites regularly post about celebrities in revealing outfits:

- **TheFashionSpot** (thefashionspot.com): High-quality fashion photos of celebs in revealing outfits. URL pattern: `/fashion-news/{id}-{slug}/`. Images from Getty Images CDN.
- **Harper's Bazaar** (harpersbazaar.com): Fashion articles with Getty Images. Pattern: `/celebrity/latest/{id}-{slug}/`.
- **inStyle** (instyle.com): Celebrity fashion articles with high-quality photos.
- **WWD** (wwd.com): Celebrity style galleries.
- **Reality Tea** (realitytea.com): Articles about celebrity revealing fashion.
- **The Sun** (the-sun.com): Celebrity fashion news with photos from `s-uk.illumservice.com` CDN.
- **MexicoYa** (mexicoya.com.mx): High-volume photo gallery site, posts multiple articles per celebrity. Image URLs follow WordPress pattern: `https://mexicoya.com.mx/wp-content/uploads/{year}/{month}/{IMG_XXXX}.jpeg`. Multiple articles per person (bikini, fashion, travel). Download with curl but convert `.jpeg` extension to `.jpg` in filename.
- **CelebMafia** (celebmafia.com): Celebrity fashion/photos gallery. WordPress images at `/wp-content/uploads/{year}/{month}/{slug}-{n}.jpg`. Per-celebrity tag pages at `/tag/{celeb-name}/`. 800-1200px wide images.
- **FTV News** (ftvnews.com.tw): Taiwanese news site with celebrity photography. Images hosted on `cdn.ftvnews.com.tw` at specific article URLs (not extractable via regex). Use `web_fetch` on article pages to extract.
- **Zoom TV** (zoomtventertainment.com): India entertainment site with celebrity photo galleries. Thumbnail URLs may all resolve to same placeholder; try fetching article to find actual image URLs.

## Indian Entertainment/Gallery Sites

These sites host Indian celebrity/model content including web series photos and biographical galleries:

- **televisiondrama.in**: Blogger-hosted Indian entertainment blog with comprehensive web series lists and photos per celebrity. Images at `blogger.googleusercontent.com/img/b/{HASH}/s1280/{file}.jpg` (full-size, 1280px wide) or `/s16000-rw/{file}.jpg` (thumbnail). Each article may have 10-20+ photos per celebrity covering individual web series. Useful for finding promotional photos from web series appearances.
- **Enigmatixmedia** (enigmatixmedia.com): Professional media/artist directory with actor profiles. Full-size images at `https://www.restapi.enigmatixmedia.com/static/images/full/{id}.jpg`, Thumbnails at `/static/images/thumb/{id}.jpg`. Profile pages at `/{username}/photos`. May have bio, filmography, and photos.
- **StarsUnfolded** (starsunfolded.com): Celebrity biography site with body measurements, filmography, and photos. WordPress images at `https://starsunfolded.com/wp-content/uploads/{year}/{month}/{name}.jpg`. Useful for biographical data and promotional photos.
- **videocelebs.net**: Video gallery index with screenshot thumbnails. Screenshot URL pattern: `/contents/videos_screenshots/{range}/{id}/source/{n}.jpg` (e.g., `{range}` is like 80000, 103000 based on video ID range). Each video page has multiple screenshots (7-15+). Use `web_fetch` markdown format to extract screenshot URLs from video pages.
- **Braflix** (braflix.bz): Adult content platform. Cast pages at `/cast/{id}-{username}`. May have poster/thumbnail images.
- **Postcredit** (postcredit.tv): Indian movie/TV database with cast profiles. May have profile pictures.
- **MXMaal** (mxmaal.com): Indian adult content directory. Model pages at `/model/` with A-Z listing. Check for profile images.

## Quality Notes

- News/reblog sites typically host resized images (600-1200px wide). They are copies of the original from the person's Instagram/social media.
- Full-size originals are usually on the source platform (Instagram) and may require downloading from there directly.
- Look for `data-orig`, `srcset`, or `data-src` attributes for higher quality variants.
- **Blogger/Blogspot images**: Use `/s1280/` path segment for 1280px wide full-size vs `/s800/` or `/s400/` for smaller. `/s16000-rw/` is the Blogger CDN internal resize — not the URL path segment.

## Pitfalls

- **Image URLs may be relative** — e.g. `/upload/2026/05/...` on allkpop needs the domain prepended.
- **Lazy loading** — some sites use `data-src` or `data-lazy` instead of `src`. Check for these.
- **Ads masquerade as images** — filter out URLs containing `ad`, `banner`, `placeholder`, `logo`, `pixel`, or third-party ad domains.
- **Google Images redirects** — going directly to `google.com/imagesearch` may hit a redirect or CAPTCHA. Use `web_search` for text results, then follow to source sites.
- **Context exhaustion** — a single `web_fetch` of a news article HTML can be 50-300KB. Budget accordingly to avoid premature sub-agent termination.
- **Yahoo articles fail with `curl | grep`** — Yahoo (and other AOL-media sites) return zero image URLs via regex extraction, likely due to JavaScript-rendered images or external CDNs. When `curl | grep` returns nothing, fall back to `web_fetch` with markdown format or og:image extraction.
- **Avoid complex download loops** — when downloading many images, prefer simple batch scripts with known URLs over inline URL construction with nested `curl` calls, which can create duplicate/badly-named files.
- **Verify downloaded files are actual images** — some sites (e.g. `bodysizex.com`, `celebsta.com`, `famousages.com`) redirect `.jpg` URLs to HTML pages. After downloading, use `file <filepath>` to verify the content is an image (e.g. `JPEG image data`). Remove files that are HTML documents.

## Video Extraction Tips

- **XHamster** (xhamster.com): gallery-dl does NOT support xHamster video URLs (only has extractors for photo galleries and user gallery pages). Use `yt-dlp` directly with the video URL. Videos use HLS streaming (m3u8 manifests), so yt-dlp should work without extra tools. Video IDs are embedded in HTML URLs: `xhamster.com/videos/{title}-{id}`.
- **Adult tubes generally**: Most tube sites deliver videos via HLS/m3u8. `yt-dlp` is reliable for these. Gallery-dl only supports a subset of sites for videos.
