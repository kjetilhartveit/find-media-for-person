---
name: using-gallery-dl
description: Use when you need to download media from websites using gallery-dl, a CLI tool supporting 100+ sites including Instagram, TikTok, Erome, Reddit, Fapello, and more.
---

# When to use this skill

- Downloading media from a site that gallery-dl supports (check with `gallery-dl --list-extractors`)
- You need guidance on gallery-dl configuration, flags, output settings, or cookies
- Setting up gallery-dl with proper destination directories, sleep settings, and filters
- Troubleshooting gallery-dl pitfalls (range counting, output directory bugs, cookie requirements)

# gallery-dl — Common Guidance

`gallery-dl` is a versatile CLI tool for downloading media from many websites including Instagram, TikTok, Erome, Reddit, Fapello, and [100+ more](https://github.com/morfius/gallery-dl#supported-services).

## Prerequisites

- Install: `pip install gallery-dl` or `pipx install gallery-dl`
- Keep updated: `pip install -U gallery-dl` — fixes for site API changes usually ship within days.
- Remember to use `gallery-dl --help` before using it to get a better understanding of available options.

## The `-o` Flag Is NOT Output Directory

**Important:** The `-o` / `--options` flag configures post filters (e.g. `-o "include=posts,reels"`), **not** the output directory. To set where files are saved:

- Use `-d, --destination PATH` on the command line, or
- Set `base-directory` in the extractor config

```bash
# Correct way to set destination
gallery-dl -d "/path/to/output/" "https://example.com/user/"
```

```json
// Or via config: extract "base-directory" in the extractor block
{
  "extractor": {
    "base-directory": "/path/to/output/"
  }
}
```

## Config File Pattern

Create a temporary config file for downloads (reusable across sources):

```json
{
  "extractor": {
    "base-directory": "<output-dir>",
    "directory": [],
    "sleep-request": [8, 16],
    "sleep-429": 120,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ..."
  }
}
```

- `directory: []` — download directly into base directory, no subdirectory nesting. Without this, gallery-dl creates nested folders per site/user.
- Pass with `--config /tmp/gallery-dl-config.json`

## Common Flags

| Flag                              | Purpose                                                                                  |
| --------------------------------- | ---------------------------------------------------------------------------------------- |
| `-d PATH`                         | Set output destination directory                                                         |
| `--config FILE`                   | Use external config file                                                                 |
| `--cookies FILE`                  | Use Netscape-format cookies file (`.data/cookies.txt`)                                   |
| `--no-mtime`                      | Don't set file modification time to upload date                                          |
| `--range 1-250`                   | Limit to first 250 **posts** (not individual files — carousels expand to multiple files) |
| `--restrict-filenames underscore` | Replace special chars in filenames with `_`                                              |
| `--download-archive DB_FILE`      | Skip already-downloaded files (SQLite archive)                                           |

## Pitfalls

- **`-d` is the reliable way to set output dir.** Do NOT use `-o "directory=[<name>]"` — it splits each character of `<name>` into a separate nested folder (e.g. `[instagram]` becomes `[/i/n/s/t/a/g/r/a/m/]`). Create the output folder first (`mkdir -p <output-dir>`) and use `-d <output-dir>`.
- **`--range` counts posts, not files.** A carousel post with 5 images counts as 5 separate files. `--range 1-1000` can yield 2000–2500+ files for profiles with many carousels. Use `--range 1-250` to stay reasonable.
- **"Trying fallback URL #1" messages are normal.** Videos often use fallback URLs; gallery-dl handles this automatically. These are informational, not errors.
- **Long downloads need long bash timeouts.** Profile downloads can take 10+ minutes. Set bash timeout to at least `900000`ms.
- **Very long downloads should be detached.** Multi-hour profile downloads exceed even large tool timeouts; agent shells often kill the whole process group on timeout, taking the background job with them. Launch truly detached and poll a log file instead:

  ```bash
  setsid nohup gallery-dl ... > /tmp/dl.log 2>&1 < /dev/null &
  tail /tmp/dl.log   # poll periodically
  ```
- **Killing a download with `pkill -f <pattern>` can kill your own shell.** The `bash -c` wrapper running `pkill` contains the pattern in its own command line, so `pkill -f` can match and kill the calling shell (symptom: the kill command hangs or "times out"). Use the PID instead — capture `$!` when launching the detached job and `kill <pid>` — or use the bracket trick so the literal pattern in your own command line doesn't match, e.g. `pkill -f "gallery-dl.*usernam[e]"`.
- **Cookies may be needed.** Some sites (Instagram, private accounts) require authentication. Pass `--cookies .data/cookies.txt`.

## Supported Sites

Some commonly useful extractors:

- instagram
- tiktok
- erome
- fapello
- reddit
- twitter
- pinterest
- flickr
- deviantart

A full list is at https://github.com/morfius/gallery-dl#supported-services.

### Checking Supported Sources

To verify that `gallery-dl` supports the target source(s), use the command `gallery-dl --list-extractors` with `grep`.
