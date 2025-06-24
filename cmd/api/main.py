#This file is for coding up a query for the chess API for a specific player
#Step by step:
#1. find out the chess api end point that is needed
#2. figure out how to code up something that will call the chess api with the given parameters
#3. figure out how to print that out for now

#API endpoint needed to query the information for the player:
#https://api.chess.com/pub/player/hikaru
# import requests
# api_url = "https://api.chess.com/pub/player/hikaru"
# response = requests.get(api_url)
# print(response.json())


import requests
import json

api_url = "https://api.chess.com/pub/player/hikaru"

headers = {
    "User-Agent": (
        "chess-leaderboard-demo/0.1 "
        "(https://github.com/yourGitHub; contact: you@example.com)"
    )
}

resp = requests.get(api_url, headers=headers, timeout=10)

print("Status:", resp.status_code)
if resp.ok:
    print(json.dumps(resp.json(), indent=2))
else:
    print(resp.text[:200])      # peek at the body for clues
