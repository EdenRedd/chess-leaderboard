import boto3
import requests
import json
import sys
from cmd.ingest.playerData import playerData
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
        playerJson = resp.json().keys()
        return playerJson

def store_players_to_dynamo(players):
    dynamodbService = boto3.resource('dynamodb')
    table = dynamodbService.Table('chess-leaderboard-players')