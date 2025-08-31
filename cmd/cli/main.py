#API endpoint needed to query the information for the player:
#https://api.chess.com/pub/player/hikaru

from pathlib import Path
import requests
import json
import sys
from cmd.ingest.playerData import playerData
import boto3

dynamodbService = boto3.resource('dynamodb')
table = dynamodbService.Table('chess-leaderboard-players')
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
    playerJson = resp.json().get("daily", [0])[0]
    print(playerJson)
    playerDataObject = playerData.from_json(playerJson)

    table.put_item(Item={"hash_key": f"daily#{playerDataObject.country}", "range_key": f"{playerDataObject.rank}#{playerDataObject.id}" })
    
    print(playerDataObject)
else:
    print(resp.text[:200])


#How are we going to manage the ingest I believe the best way to do it would be to do it by 

