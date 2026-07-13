#!/usr/bin/env bash
URL="https://battlevive.pages.dev/api/matchmaking/join-lobby"
TOKEN="$(tr -d '\r\n' < token.txt)"
while true; do
curl -sS -i -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  --data '{"lobbyId":62,"slot":"team_one","password":""}'
curl -sS -i -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  --data '{"lobbyId":62,"slot":"team_two","password":""}'


done

