# Skill: find-media-from-xasiat

# When to use this skill

- Downloading leaked videos from Xasiat (xasiat.com) featuring specific models/pornstars
- Searching for content by model name on Xasiat
- Scraping Xasiat album/video pages using gallery-dl or yt-dlp

# Find media from Xasiat (xasiat.com)

Xasiat is an aggregator of leaked adult content, particularly Asian models. Content is organized by model and album.

## URL Patterns

- **Model profile**: `https://www.xasiat.com/albums/models/MODEL/` or `https://www.xasiat.com/fr/models/MODEL/` (French locale)
- **Model RSS feed**: `https://www.xasiat.com/rss/models/MODEL/`
- **Model search**: `https://www.xasiat.com/search/QUERY/`
- **Video page**: `https://www.xasiat.com/videos/VIDEO_ID/TITLE/`
- **Album page**: `https://www.xasiat.com/albums/ALBUM_ID/TITLE/`
- **Tags**: `https://www.xasiat.com/tags/TAG_NAME/`
- **Categories**: `https://www.xasiat.com/categories/CATEGORY/`

## Model page discovery

Model pages show content organized into sections like "Top Models", "Top Categories", and the specific model's section. Content is grouped by section headings (h4 tags). Video URLs follow the pattern `/videos/NUMBER/TITLE/`.

Videos on the model page may include both the target model's content AND related/recommended videos from the same collection. **Verify each video** by checking the title and description for the model's name. Videos without the model's name in the title/description may be from a different model entirely.

## Extractors

### gallery-dl

- **XasiatModelExtractor**: `https://www.xasiat.com/albums/models/MODEL/`
  - Note: The async block endpoint may return 404 in headless environments. Content may not be fully discoverable via gallery-dl.
- **XasiatSearchExtractor**: `https://www.xasiat.com/search/QUERY/`
  - Note: The async block endpoint may also return 404 for search results.
- **XasiatAlbumExtractor**: `https://www.xasiat.com/albums/ALBUM_ID/TITLE/`

### yt-dlp (recommended for videos)

```bash
# Download from model profile
yt-dlp --restrict-filenames -o "%(title)s.%(ext)s" \
  "https://www.xasiat.com/albums/models/MODEL/"

# Download individual video
yt-dlp --restrict-filenames -o "%(title)s.%(ext)s" \
  "https://www.xasiat.com/videos/12345/TITLE/"

# Download multiple videos at once
yt-dlp --restrict-filenames -o "%(title)s.%(ext)s" \
  --no-playlist \
  "https://www.xasiat.com/videos/ID1/TITLE1/" \
  "https://www.xasiat.com/videos/ID2/TITLE2/"
```

## Video pages often show content from multiple models/collections

When scraping a model page, the HTML may list videos in section blocks. Some videos may be from different models. Always verify:
1. Video title matches the model name
2. Description matches the model name (shows model name, not just "Thaiswinger" or collection name)

## Thumbnails and preview

Video previews are available at:
`https://www.xasiat.com/get_file/CATEGORY/HASH/DIRECTORY/VIDEO_ID/VIDEO_ID_preview.mp4/`

Example: `https://www.xasiat.com/get_file/10/376a31b278f571abb79944f5dc25f089/14000/14444/14444_preview.mp4/`

## Tags commonly associated with Asian models

Teen, Thai, Chinese, Japanese, Hardcore, Creampie, Anal, Blowjob, POV, Homemade, Babes, Big Tits, Asian, Brunette, Girlfriend, Solo, Small Tits, Sl