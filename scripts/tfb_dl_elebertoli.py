#!/usr/bin/env python3
"""
Download Eleonora Bertoli images from TheFappeningBlog.com.
Extracts gallery thumbs from listing pages, converts to full-size URLs, downloads.
"""
import re, os, time
from urllib.request import Request, urlopen

BASE = "https://thefappeningblog.com"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
DEST = "/mnt/laptop-mediaperson/elebertoli 2026-08-14 03-39-25/thefappeningblog"

def grab(url):
    try:
        with urlopen(Request(url, headers={"User-Agent": UA}), timeout=30) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  ERROR: {e}", flush=True)
        return None

def to_fullsize(thumb):
    if not thumb: return None
    if "_350px.jpg" in thumb:
        return thumb.replace("_350px.jpg", ".jpg")
    return thumb

def dl(path, url):
    for _ in range(3):
        try:
            with urlopen(Request(url, headers={"User-Agent": UA}), timeout=30) as r:
                data = r.read()
                if len(data) < 5000:
                    return False, f"tiny ({len(data)}b)"
                with open(path, "wb") as f:
                    f.write(data)
                return True, len(data)
        except:
            if _ < 2: time.sleep(2)
    return False, "max retries"

def main():
    os.makedirs(DEST, exist_ok=True)
    items = []

    for url, label in [
        (BASE+"/gallery/eleonora-bertoli/", "main"),
        (BASE+"/gallery/eleonora-bertoli/page-2/", "page2"),
        (BASE+"/gallery/eleonora-bertoli/page-3/", "page3"),
        (BASE+"/gallery/eleonora-bertoli/page-4/", "page4"),
        (BASE+"/gallery/eleonora-bertoli/page-5/", "page5"),
    ]:
        print(f"[*] {label}", flush=True)
        html = grab(url)
        if not html: continue
        pat = r'<div class="item_content">\s*<a\s+href="[^"]*/gallery/eleonora-bertoli/(\d+)/"[^>]*>\s*<div[^>]*>\s*<img[^>]*src="([^"]+)"'
        found = re.findall(pat, html, re.DOTALL)
        seen = set()
        for num_s, thumb in found:
            n = int(num_s)
            if n not in seen:
                seen.add(n)
                full = to_fullsize(thumb)
                if full: items.append((n, full))
        print(f"    {len(found)} items (+{len(items)-sum(1 for _ in items if _[0]<=0)}) total", flush=True)
        time.sleep(0.5)

    items.sort(key=lambda x: x[0], reverse=True)
    print(f"\n[*] Total: {len(items)} galleries", flush=True)
    existing = set(os.listdir(DEST))
    print(f"[*] Existing: {len(existing)} files", flush=True)

    dl_n = skip = fail = 0
    fails = []
    for i, (num, url) in enumerate(items):
        if (i+1) % 30 == 0:
            print(f"[{i+1}/{len(items)}] {dl_n}DL {skip}skip {fail}fail", flush=True)
        fname = f"elebertoli_gallery_{num:03d}.jpg"
        if fname in existing:
            skip += 1; continue
        ok, info = dl(os.path.join(DEST, fname), url)
        if ok:
            dl_n += 1
            print(f"  #{num} OK {info}b -> {fname}", flush=True)
        else:
            fail += 1; fails.append((num, info))
            print(f"  #{num} FAIL {info}", flush=True)
        time.sleep(0.4)

    print(f"\n{'='*60}")
    print(f"TOTAL={len(items)} DL={dl_n} SKIP={skip} FAIL={fail}")
    if fails: print(f"FAILURES: {fails}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()