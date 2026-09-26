#!/usr/bin/env python3
"""List files in the SourceForge 'bitcoin' project using a real Chrome via
Playwright (plain curl gets a Cloudflare 403). Low volume, polite delays."""
import sys, time, json
from playwright.sync_api import sync_playwright

paths = sys.argv[1:] or ["Bitcoin/"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page()
    for path in paths:
        url = f"https://sourceforge.net/projects/bitcoin/files/{path}"
        pg.goto(url, wait_until="domcontentloaded", timeout=60000)
        time.sleep(4)
        rows = pg.eval_on_selector_all("table#files_list tbody tr", """rows => rows.map(r => {
            const a = r.querySelector('th a, td a'); const t = r.querySelector('abbr');
            return {name: r.getAttribute('title'), href: a ? a.href : null, date: t ? t.getAttribute('title') : null,
                    size: (r.querySelector('td[headers=files_size_h]')||{}).innerText || null}; })""")
        print(json.dumps({"url": url, "title": pg.title(), "rows": rows}, indent=1))
        time.sleep(3)
    b.close()
