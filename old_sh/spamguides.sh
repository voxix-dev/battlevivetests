#!/usr/bin/env bash
TOKEN="$(tr -d '\r\n' < token.txt)"
while true; do
	curl -X POST 'https://usfuamngimwsnnfemhsl.supabase.co/rest/v1/guides' \
  -H 'apikey: 'sb_publishable_1l5bqXxHuewHwBBs6CqrYw_Zs5QbjfZ'' \
  -H 'Authorization: Bearer '"$TOKEN"'' \
  -H 'Content-Type: application/json' \
  -H 'Prefer: return=representation' \
  -d '{
    "champion":"Raigon",
    "title":"Never gonna give you up",
    "body":"\"</p><img src=\"https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic1.srcdn.com%2Fwordpress%2Fwp-content%2Fuploads%2F2021%2F02%2FRick-Astley-Never-Gonna-Give-You-Up-Remastered-Header.jpg&f=1&nofb=1&ipt=d97d282d6f838f912f76d004148aa119a8849942086870f94543e75001917f0d\"> <p>",
    "author_id":"713c42a3-1516-4704-96d0-b989c9130940",
    "updated_at":"6969-06-07T21:37:00.488Z"
  }'
done

