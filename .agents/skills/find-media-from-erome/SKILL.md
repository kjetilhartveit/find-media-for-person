---
name: find-media-from-erome
description: Use when you need to find and download media from Erome, a user-hosted adult content sharing site with albums.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for albums of a specific person on Erome
- Searching Erome user pages for media
- Searching Erome by query to find albums matching a person
- Downloading images and videos from Erome albums or user pages

# Find media from Erome

Download images and videos from Erome (https://www.erome.com), a user-hosted adult content sharing platform.

`gallery-dl` has a built-in `EromeAlbumExtractor`, `EromeUserExtractor`, and `EromeSearchExtractor` — use this as the **primary** download method. Fall back to manual parsing only when `gallery-dl` fails.

## URL Patterns

- Site: `https://www.erome.com`
- Search: `https://www.erome.com/search?q={name}`
- Album pages: `https://www.erome.com/a/{album_id}` (e.g., `erome.com/a/fwBHXEGc`)
- User pages: `https://www.erome.com/USER`
- Media served from: `https://s{number}.erome.com/{user_id}/{album_id}/{file_id}.jpg`

## Primary download method — Download via gallery-dl

`gallery-dl` handles Erome natively with 3 extractors: `EromeAlbumExtractor`, `EromeUserExtractor`, `EromeSearchExtractor`. It resolves all media URLs, filters thumbnails, and downloads files with no auth required.

## Fallback download method — Manual parsing and download

When gallery-dl is unavailable or fails:

1. **Search** for the person's name on `https://www.erome.com/search?q={name}` — results include album cards with titles and engagement metrics. Look for album links matching `/a/{album_id}`.
2. **Parse album pages**
   - Extract `data-src` and `src` attributes from `<img>` tags — these point directly to full-size media on `s{number}.erome.com`.
   - Filter out any URLs containing `/thumbs/` — those are thumbnails.
   - No URL pattern guessing needed; the `data-src`/`src` attributes provide the actual full-size URLs directly.
3. **Download media** with `Referer: https://www.erome.com/` header and rate-limit to 0.3–0.5s between requests.
4. Prefix filenames with the album ID to avoid collisions (Erome files have random IDs).

## Quality

- **Images**: modest quality, files range from ~10KB to ~300KB, typically 480–576px wide, occasional higher-res (up to 1280×720 observed).
- **Videos**: typically 720p quality, can be large (1MB–17MB+). Videos are served from `v{number}.erome.com` with `_720p.mp4` suffix.
- Some video albums contain very large individual files (e.g., "Absolute perfection" by TheGoat47: 25+ videos totaling 650MB+ from a single album).
- Content quality varies significantly by uploader.
- Some content is from dedicated content creators/farms (e.g., "Gloryhole-Top-Secrets", "Gangbang-Creampie-Secrets", "PrettyDirtySluts") that post multiple albums per person.
- Some uploaders post bulk compilations of content: users like `8704`, `8713`, `5913`, `3899` post large albums (80-95 images) per person, often titled generically. These are fan compilations rather than original content.
- Some albums contain both image (.jpg) and video (.mp4) files with the same base filename ID. The images are single-frame thumbnails/screenshots of the videos. Gallery-dl downloads both, so you get redundant content. Consider downloading only videos for efficiency.
- Some albums contain ONLY image files that are thumbnails from videos. The actual video content may not be available for those albums. Always check `gallery-dl --get-urls` first to see what is available.

## Known Sources with High-Value Content

- **Gloryhole-Top-Secrets**: Posts multiple albums per person focusing on facial/cumshot content.
- **Gangbang-Creampie-Secrets**: Post gangbang/creampie themed content.
- **PrettyDirtySluts**: Posts explicit solo/couple content.
- **ESPOSASAFADINHA**: Posts leaked/personal content.
- **GoingOutofBusiness**: Posts studio/performance content.
- **TheWatcher77**: Posts celebrity content in "Keep the Beat" themed albums.
- **tcr31**: Aggregator with bulk celebrity albums.
- **BlackTittyBear**: Posts celebrity content in dedicated albums.
- **djkidrich**: Posts large collections (100+ images) of celebrity content.
- **Digitaldash**: Posts celebrity PMV and edited content.
- **Celebs_Trending**: Posts trending celebrity content with emojis in titles.
- **funika**: Posts Romanian celebrity content in compilations (e.g., "ROMANIAN FAMOUS BEAUTYS WHO WOULD LOOK HOT IN A PORN SCENE") and solo albums. Tags albums with person name.
- **miillffss**: Posts dedicated albums per person (e.g., "INNA LOVE 1", "INNA LOVE 3") with large image sets (35-78 images per album).
- **Dclotta**: Posts INNA music video re-edits (e.g., "INNA - 'INNdiA' MV [Sexy Lesbian Re-Edit]", "INNA - 'Cola Song' [Bikini Dancing Edit]").
- **Zwood007**: Posts German model content in series (e.g., "Inna Blank 52yo German slut", "Inna Blank 53 Brandenburg").

## Download Filtering Tips

- After downloading, filter files by checking filename for the person's name.
- Remove incomplete downloads (.part files) after filtering.
- Inspect results before bulk downloading: use `gallery-dl -J URL` to dump JSON and `gallery-dl --get-urls URL` to see album list first.
- Filter out AI-generated content: users like `AiCelebrityy`, `ThaHxncho`, `Xgalicialol`, `Botman32`, `KustomEditz`, `ggt1748` frequently post AI/fake content, not real media of the person.
- Filter out non-relevant "Tyla" variants: search results often include content about different people named "Tyla" (Tyla Wynn, Coco Tyla, Tyla Moore, Tyla Tyler, etc.).
- **Search term "jiji" is extremely noisy**: Returns unrelated results including Spanish slang "jiji" (giggle), user names like "LadyboysFuckedBareback Jiji", and completely unrelated content. Only search with "jijiwonder" or "jiji+wonder" for better precision. When searching "jiji" alone, most results are false positives.
- **Search term "wonder" alone is extremely noisy**: Returns 36+ albums with the word "wonder" in various contexts (wonder woman, one-hit wonder, etc.). Always use "jiji" + "wonder" together for precise results.
- Filter out other-name variants: common names like "Inna" often return results for multiple people (German models named Inna, Ukrainian models, adult entertainers, etc.). Use tags like `#romania`, album titles mentioning singer/music, or user source to distinguish.
- Filter out "inna" as slang: the word "inna" (slang for "in a") appears in many unrelated album titles (e.g., "Sucking dick inna car!", "cumtribute inna spot"). These are noise, not the person's name. Look for capitalized "INNA" or clear person references.
- Content farm albums like "BJ Toy" by `Giltypleasure` or "gyrate" by `Giltypleasure` often appear in search results but are unrelated ads.
- For high-volume searches, consider downloading album-by-album in batches rather than all at once (search results can return 48+ albums).
- **Multiple search term variants**: Try compact/abbreviated/underscored/hyphenated variants of the name as they may return different or more comprehensive results across albums.
- **Album images vs videos**: Some albums have both images and videos sharing the same filename ID (images are frame thumbnails). When gallery-dl downloads such albums, both are saved. For space efficiency, you can filter to keep only videos (which contain the full content).
- gallery-dl output file structure varies: some albums create `USERNAME/FILENAME` (flat), others `USERNAME/ALBUM_ID Filename` (nested). Handle both patterns when moving files.

## Pitfalls

- Album pages may be behind Cloudflare protection in some cases.
- Erome filenames are random IDs — no semantic naming for downloaded files.
- Search results per person can be very large (48+ albums), leading to timeouts; download in batches.
- Some albums may have duplicate images shared across albums.
- Video downloads can be slow due to file sizes; consider rate-limiting for large batches.
- Gallery-dl search downloads handle all albums at once; individual album downloads can be used for targeted fetching.
- Gallery-dl `-d` destination argument can create nested directory structures (`erome/erome/`) in certain invocation patterns — flatten after download.
- When using `gallery-dl -i` with an input file of URLs, the download destination parameter may create a nested `erome/` directory that needs flattening.
