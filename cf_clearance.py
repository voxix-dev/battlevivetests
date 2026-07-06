#!/usr/bin/env python3
import sys
import json
import os

def get_cf_clearance() -> str:
    AUTH_FILE = "playwright/.auth/state.json"
    if not os.path.exists(AUTH_FILE):
        print(f"Missing: {AUTH_FILE}. Run save_state.py first.")
        sys.exit(1)
    with open(AUTH_FILE, "r") as f:
        state = json.load(f)
    for cookie in state.get("cookies", []):
        if cookie["name"] == "cf_clearance" and cookie["domain"] == ".battlevive.com":
            cf_clearance = cookie["value"] 
    return cf_clearance

print(get_cf_clearance())
