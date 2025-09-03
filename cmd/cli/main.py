#API endpoint needed to query the information for the player:
#https://api.chess.com/pub/player/hikaru

from pathlib import Path
import requests
import json
import sys
from cmd.ingest.playerData import playerData
import boto3

#separate the logic of calling the api 
#separate the logic of calling the database to store the info
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
    playerJson = resp.json().get("daily")
    for item in playerJson:
        print(item)
        playerDataObject = playerData.from_json(item)

    
        countryRequest = requests.get(playerDataObject.country, headers=headers, timeout=10)
        countryResponseJson = countryRequest.json().get("code")
        playerRequest = requests.get(playerDataObject.id, headers=headers, timeout=10)
        print("================")
        print(playerRequest)
        playerResponseJson = playerRequest.json().get("player_id")


        table.put_item(Item={"hash_key": f"daily#{countryResponseJson}", "range_key": f"{playerDataObject.rank}#{playerResponseJson}", "player_id": f"{playerResponseJson}", "url": f"{playerDataObject.url}", "username": f"{playerDataObject.username}", "score" : f"{playerDataObject.score}", "rank": f"{playerDataObject.rank}", "country": f"{playerDataObject.country}", "name": f"{playerDataObject.name}", "status": f"{playerDataObject.status}", "avatar": f"{playerDataObject.avatar}", "flair_code": f"{playerDataObject.flair_code}", "win_count": f"{playerDataObject.win_count}", "loss_count": f"{playerDataObject.loss_count}", "draw_count": f"{playerDataObject.draw_count}" })
    
    #print(playerDataObject)
else:
    print(resp.text[:200])


#How are we going to manage the ingest I believe the best way to do it would be to do it by 

