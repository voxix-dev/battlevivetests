#!/usr/bin/env bash

SUPABASE_URL="https://usfuamngimwsnnfemhsl.supabase.co"
SUPABASE_API_KEY="sb_publishable_1l5bqXxHuewHwBBs6CqrYw_Zs5QbjfZ"
TOKEN="$(tr -d '\r\n' < token.txt)"

curl -G "${SUPABASE_URL}/rest/v1/lobbies" \
  -H "apikey: ${SUPABASE_API_KEY}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json"\
echo 
   

