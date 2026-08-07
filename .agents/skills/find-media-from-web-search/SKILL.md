---
name: find-media-from-web-search
description: Find media via Google Images and web search by discovering article URLs, then extracting image URLs efficiently.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

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

## Quality Notes

- News/reblog sites typically host resized images (600-1200px wide). They are copies of the original from the person's Instagram/social media.
- Full-size originals are usually on the source platform (Instagram) and may require downloading from there directly.
- Look for `data-orig`, `srcset`, or `data-src` attributes for higher quality variants.

## Pitfalls

- **Image URLs may be relative** — e.g. `/upload/2026/05/...` on allkpop needs the domain prepended.
- **Lazy loading** — some sites use `data-src` or `data-lazy` instead of `src`. Check for these.
- **Ads masquerade as images** — filter out URLs containing `ad`, `banner`, `placeholder`, `logo`, `pixel`, or third-party ad domains.
- **Google Images redirects** — going directly to `google.com/imagesearch` may hit a redirect or CAPTCHA. Use `web_search` for text results, then follow to source sites.
- **Context exhaustion** — a single `web_fetch` of a news article HTML can be 50-300KB. Budget accordingly to avoid premature sub-agent termination.
- **Yahoo articles fail with `curl | grep`** — Yahoo (and other AOL-media sites) return zero image URLs via regex extraction, likely due to JavaScript-rendered images or external CDNs. When `curl | grep` returns nothing, fall back to `web_fetch` with markdown format or og:image extraction.
- **Avoid complex download loops** — when downloading many images, prefer simple batch scripts with known URLs over inline URL construction with nested `curl` calls, which can create duplicate/badly-named files.
- **Verify downloaded files are actual images** — some sites (e.g. `bodysizex.com`, `celebsta.com`, `famousages.com`) redirect `.jpg` URLs to HTML pages. After downloading, use `file <filepath>` to verify the content is an image (e.g. `JPEG image data`). Remove files that are HTML documents.
