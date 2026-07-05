#!/usr/bin/env python3
"""
Run headlessly, reusing the saved storage state from save_state.py.
No OAuth flow, no Turnstile challenge — already authenticated.
"""
from playwright.sync_api import sync_playwright

AUTH_FILE = "playwright/.auth/state.json"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(storage_state=AUTH_FILE)
    page = context.new_page()

    page.goto("https://battlevive.com/")

    # Your assertions / test steps go here.
    print(page.title())

    browser.close()
