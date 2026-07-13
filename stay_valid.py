#!/usr/bin/env python3
"""
Run once, headed, to complete Discord OAuth manually.
Saves authenticated browser state to playwright/.auth/state.json
"""
import requests
# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright
import json
import os
import sys
# pyrefly: ignore [missing-import]
from apscheduler.schedulers.blocking import BlockingScheduler
import requests

SUPABASE_API_KEY = "sb_publishable_1l5bqXxHuewHwBBs6CqrYw_Zs5QbjfZ" 


AUTH_FILE = "playwright/.auth/state.json"
SUPABASE_URL = "https://usfuamngimwsnnfemhsl.supabase.co"
class TokenManager:
    def __init__(self, JWT_token, refresh_token):
        self.JWT_token = JWT_token 
        self.refresh_token = refresh_token
    
    def revalidate(self, refresh_token):
        
        headers = {
            "Content-Type": "application/json",
            "apikey": SUPABASE_API_KEY
        }
        json = {
            "refresh_token": refresh_token 
        }
        response = requests.post(f"{SUPABASE_URL}/auth/v1/token?grant_type=refresh_token", headers=headers, json=json)
        data=response.json()
        new_refresh_token =data["refresh_token"] 
        new_JWT_token= data["access_token"] 
        print("Revalidating tokens!...")
        print(f"New refresh token: {new_refresh_token} \n New JWt token: {new_JWT_token}")
        return new_refresh_token,new_JWT_token  

    def revalidate_tokens(self):
        new_refresh_token,new_JWT_token= self.revalidate(self.refresh_token)
        self.refresh_token = new_refresh_token
        self.JWT_token = new_JWT_token

def save_state():
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=AUTH_FILE)
        page = context.new_page()
    
        page.goto(f"{SUPABASE_URL}/auth/v1/authorize?provider=discord&redirect_to=https%3A%2F%2Fbattlevive.com%2Fauth%2Fcallback")
    
        # Click your site's "Login with Discord" button, then log in
        # and approve the OAuth consent screen manually in the opened window.
        input("Complete login in the browser, then press Enter here...")
    
        context.storage_state(path=AUTH_FILE)
        browser.close()

def get_JWT_token() -> str:
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
def get_refresh_token():
    with open(AUTH_FILE, "r") as f:
        state = json.load(f)
    
    for origin in state.get("origins", []):
        if origin["origin"] != "https://battlevive.com":
            continue
        for item in origin.get("localStorage", []):
            if item["name"] == "sb-usfuamngimwsnnfemhsl-auth-token":
                auth_data = json.loads(item["value"])
                token = auth_data["refresh_token"]
    return token
def test_request(JWT_token):
    url = f"{SUPABASE_URL}/rest/v1/lobbies"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {JWT_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url=url,headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        print(response.json())
    

def main():
    save_state()
    tokens = TokenManager(JWT_token=get_JWT_token(),refresh_token=get_refresh_token())
    tokens.revalidate_tokens()
    test_request(tokens.JWT_token)
    scheduler = BlockingScheduler()
    scheduler.add_job(tokens.revalidate_tokens, 'interval', minutes=30)
    scheduler.add_job(test_request,'interval',minutes=5, args=[tokens.JWT_token])
    scheduler.start()

if __name__ == "__main__":
    main()
