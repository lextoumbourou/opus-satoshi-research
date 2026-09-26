#!/usr/bin/env python3
"""Fetch a page with headless Chrome (Playwright) and save the rendered HTML
and innerText. Usage: fetch_rendered.py URL OUT_PREFIX"""
import sys, time
from playwright.sync_api import sync_playwright
url, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--disable-blink-features=AutomationControlled"])
    ctx = b.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36")
    pg = ctx.new_page()
    pg.goto(url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(6)
    open(out + ".html", "w").write(pg.content())
    open(out + ".txt", "w").write(pg.inner_text("body"))
    print(pg.title())
    b.close()
