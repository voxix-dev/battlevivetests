#!/usr/bin/env python3
import json

AUTH_FILE = "playwright/.auth/state.json"

with open(AUTH_FILE, "r") as f:
    state = json.load(f)

for origin in state.get("origins", []):
    if origin["origin"] != "https://battlevive.com":
        continue
    for item in origin.get("localStorage", []):
        if item["name"] == "sb-usfuamngimwsnnfemhsl-auth-token":
            auth_data = json.loads(item["value"])
            print("JWT:", auth_data["access_token"])
