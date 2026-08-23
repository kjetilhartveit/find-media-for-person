# Skill: find-media-from-pornpics

# When to use this skill

- Downloading photo galleries from pornpics.com (large adult photo gallery site)
- Searching for image galleries on pornpics.com by model name

# Main website

- Base URL: https://www.pornpics.com/
- Pornstar pages: `https://www.pornpics.com/pornstars/{name}/`
- Search: `https://www.pornpics.com/?q={query}`
- Tags: `https://www.pornpics.com/tags/{tag}/`

# Key features

- **gallery-dl supported**: Use `gallery-dl` to download all galleries from a pornstar page or search results
- 16-20 images per gallery typically
- Sites use image IDs (numeric) for gallery organization
- Gallery directories are named by ID number

# How to download

## Using gallery-dl (recommended)

```bash
# Download all galleries for a pornstar
gallery-dl "https://www.pornpics.com/pornstars/{name}/"

# Download from search results (may find more galleries)
gallery-dl "https://www.pornpics.com/?q={name}+facial"

# With config for rate limiting
echo '{"extractor": {"threads": 2}}' > ~/.config/gallery-dl/gallery-dl.conf
```

## Output

- Files named `pornpics_{gallery_id}_{img_number}.jpg`
- Organized in subfolders by gallery ID

# Notes

- pornpics uses its own CDN and serves high-quality images (~2MB per image)
- Some galleries include co-stars; filter for target model if needed
- Image count: typically 16-20 per gallery
- Example from Arya Fae search: 1,659 images across ~100 galleries
- **Model page limitation**: `gallery-dl "https://www.pornpics.com/pornstars/{name}/"` may download only 1 image per gallery for some models. When this happens, use the query search `gallery-dl "https://www.pornpics.com/?q={name}"` instead, which returns full galleries with all images.
- **Search is very broad**: The pornstar page downloads ALL brunette/teen galleries, not just the target model. Filter galleries AFTER download by checking names for the model name or known aliases (e.g., "Veronica" for Amber Hardin). Remove galleries with clearly different model names (e.g., "Kelly Carson", "Alice", "Brigitte D") to avoid clutter.
- Gallery IDs can be cross-referenced with other sites to identify the same gallery (e.g., gallery ID 99762708 appears on both pornpics and sexygirlspics for the same Amber Hardin gallery).