#!/usr/bin/env python3
import sys
from urllib.parse import urlparse, parse_qs
import requests
import json
import os
# Hardcode these
SUPABASE_URL = "https://usfuamngimwsnnfemhsl.supabase.co"      # e.g. "https://xxxxx.supabase.co"
SUPABASE_API_KEY = "sb_publishable_1l5bqXxHuewHwBBs6CqrYw_Zs5QbjfZ"  # e.g. anon or service_role key
BATTLEVIVE_URL = "https://battlevive.com"

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


def select_request(headers, url, select="*", filters=None, order=None, limit=None):
    params = {"select": select}
    if filters:
        params.update(filters)
    if order:
        params["order"] = order
    if limit:
        params["limit"] = str(limit)
    return requests.get(url, headers=headers, params=params)
def invite_player(targetUserID,lobbyId,token): 
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
            "lobbyId": lobbyId,
            "targetUserID" : targetUserID
    }
    print(f"Inviting : {targetUserID} to lobby: {lobbyId}")
    return requests.post(f"{BATTLEVIVE_URL}/api/matchmaking/invite-player",headers=headers,data=data) 

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

    response = select_request(headers, url, select=id) 

    print(f"Lobby Status: {response.status_code}")
    #print(response.json())

    lobbies = response.json()

    url = f"{SUPABASE_URL}/rest/v1/users"
    response = select_request(headers, url, select=id)
    print(f"Users Status: {response.status_code}")

    users = response.json()
    for lobby in lobbies:
        for user in users:
            response=invite_player(lobbyId=lobby['id'], targetUserID=user['id'],token=token)
            print(f"Invite Status: {response.status_code}")

    
   # print(users)
if __name__ == "__main__":
    main()
