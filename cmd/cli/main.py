#API endpoint needed to query the information for the player:
#https://api.chess.com/pub/player/hikaru

from pathlib import Path
import requests
import json
import sys

api_url = "https://api.chess.com/pub/leaderboards"

headers = {
    "User-Agent": (
        "chess-leaderboard-demo/0.1 "
        "(https://github.com/yourGitHub; contact: you@example.com)"
    )
}

resp = requests.get(api_url, headers=headers, timeout=10)

print("Status:", resp.status_code)
if resp.ok:
    out_path = Path("samples/players/output.txt")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(resp.json()))
    print(json.dumps(resp.json(), indent=2))
else:
    print(resp.text[:200])


#How are we going to manage the ingest I believe the best way to do it would be to do it by 

