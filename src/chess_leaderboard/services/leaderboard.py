import boto3
import requests
import json
import sys
from cmd.ingest.playerData import PlayerData
from pathlib import Path

def fetch_chess_data():
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
        gameModes = resp.json().keys()

        gameModeHash = {}
        
        for mode in gameModes:
            players = {}
            playerJson = resp.json().get(mode)
            players[mode] = []
            for item in playerJson:
                playerDataObject = PlayerData.from_json(item)
                players[mode].append(playerDataObject)
            gameModeHash[mode] = players[mode]
        return gameModeHash
        

def store_players_to_dynamo(players):
    headers = {
    "User-Agent": (
        "chess-leaderboard-demo/0.1 "
        "(https://github.com/yourGitHub; contact: you@example.com)"
    )
    }
    dynamodbService = boto3.resource('dynamodb')
    table = dynamodbService.Table('chess-leaderboard-players')
    print("About to print")
    for gameMode in players.keys():
        for item in players[gameMode]:
            print(item)
            countryRequest = requests.get(item.country, headers=headers, timeout=10)
            countryResponseJson = countryRequest.json().get("code")
            playerRequest = requests.get(item.id, headers=headers, timeout=10)
            print("================")
            print(playerRequest)
            playerResponseJson = playerRequest.json().get("player_id")
            table.put_item(Item={"hash_key": f"{gameMode}#{countryResponseJson}", "range_key": f"{item.rank}#{playerResponseJson}", "player_id": f"{playerResponseJson}", "url": f"{item.url}", "username": f"{item.username}", "score" : f"{item.score}", "rank": f"{item.rank}", "country": f"{item.country}", "name": f"{item.name}", "status": f"{item.status}", "avatar": f"{item.avatar}", "flair_code": f"{item.flair_code}", "win_count": f"{item.win_count}", "loss_count": f"{item.loss_count}", "draw_count": f"{item.draw_count}" })