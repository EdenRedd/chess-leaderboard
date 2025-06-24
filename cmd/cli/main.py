#API endpoint needed to query the information for the player:
#https://api.chess.com/pub/player/hikaru

from pathlib import Path
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
    out_path = Path("samples/players/output.txt")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(resp.json()))
    print(json.dumps(resp.json(), indent=2))
else:
    print(resp.text[:200])
