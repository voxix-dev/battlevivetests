#!/usr/bin/env python3
import sys
from urllib.parse import urlparse, parse_qs
import requests
import json
import os
# Hardcode these
SUPABASE_URL = "https://usfuamngimwsnnfemhsl.supabase.co"      # e.g. "https://xxxxx.supabase.co"
SUPABASE_API_KEY = "sb_publishable_1l5bqXxHuewHwBBs6CqrYw_Zs5QbjfZ"  # e.g. anon or service_role key

def get_access_token() -> str:
    AUTH_FILE = "playwright/.auth/state.json"
    if not os.path.exists(AUTH_FILE):
        print(f"Missing: {AUTH_FILE}. Run save_state.py first.")
        sys.exit(1)

    with open(AUTH_FILE, "r") as f:
        state = json.load(f)

    for origin in state.get("origins", []):
        if origin["origin"] != "https://battlevive.com":
            continue
        for item in origin.get("localStorage", []):
            if item["name"] == "sb-usfuamngimwsnnfemhsl-auth-token":
                auth_data = json.loads(item["value"])
                token = auth_data["access_token"]
    return token


def query_lobbies(headers, url, select="*", filters=None, order=None, limit=None):
    params = {"select": select}
    if filters:
        params.update(filters)
    if order:
        params["order"] = order
    if limit:
        params["limit"] = str(limit)
    return requests.get(url, headers=headers, params=params)


def main():
    if not SUPABASE_URL or not SUPABASE_API_KEY:
        print("Error: hardcode SUPABASE_URL, SUPABASE_API_KEY, before running.", file=sys.stderr)
        sys.exit(1)
    token = get_access_token()

    url = f"{SUPABASE_URL}/rest/v1/lobbies"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = query_lobbies(headers, url)

    print(f"Status: {response.status_code}")
    try:
        print(response.json())
    except ValueError:
        print(response.text)


if __name__ == "__main__":
    main()
