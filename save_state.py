#!/usr/bin/env python3
"""
Run once, headed, to complete Discord OAuth manually.
Saves authenticated browser state to playwright/.auth/state.json
"""
# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright

AUTH_FILE = "playwright/.auth/state.json"
SUPABASE_URL = "https://usfuamngimwsnnfemhsl.supabase.co"
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto(f"{SUPABASE_URL}/auth/v1/authorize?provider=discord&redirect_to=https%3A%2F%2Fbattlevive.com%2Fauth%2Fcallback")

    # Click your site's "Login with Discord" button, then log in
    # and approve the OAuth consent screen manually in the opened window.
    input("Complete login in the browser, then press Enter here...")

    context.storage_state(path=AUTH_FILE)
    browser.close()
