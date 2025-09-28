import boto3
import requests
import json
import sys
from chess_leaderboard.models.player import PlayerData
from pathlib import Path

def fetch_chess_data():
    api_url = "https://api.chess.com/pub/leaderboards"

    headers = {
        "User-Agent": (
            "chess-leaderboard-demo/0.1 "
            "(https://github.com/yourGitHub; contact: you@example.com)"
        )
    }

    try:
        print(f"Fetching leaderboard data from {api_url}...")
        resp = requests.get(api_url, headers=headers, timeout=10)
        print(f"HTTP status code: {resp.status_code}")

        # Check if response was successful
        if not resp.ok:
            print(f"Failed to fetch data: {resp.text}")
            return {}

        data = resp.json()
        print(f"Response keys (game modes) received: {list(data.keys())}")

        gameModeHash = {}
        for mode in data.keys():
            print(f"Processing game mode: {mode}")
            playerJsonList = data.get(mode)
            if not playerJsonList:
                print(f"No players found for game mode: {mode}")
                continue

            gameModeHash[mode] = []
            for idx, item in enumerate(playerJsonList):
                try:
                    playerDataObject = PlayerData.from_json(item)
                    gameModeHash[mode].append(playerDataObject)
                except Exception as e:
                    print(f"Error parsing player {idx} in mode {mode}: {e}")

            print(f"Total players parsed for {mode}: {len(gameModeHash[mode])}")

        print(f"Total game modes processed: {len(gameModeHash)}")
        return gameModeHash

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}
        

def store_players_to_dynamo(players):
    headers = {
    "User-Agent": (
        "chess-leaderboard-demo/0.1 "
        "(https://github.com/yourGitHub; contact: you@example.com)"
    )
    }
    dynamodbService = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodbService.Table('chess-leaderboard-players')
    print("About to print")
    for gameMode in players.keys():
        for item in players[gameMode]:
            try:
                #This needs to be optimized to avoid too many requests
                # countryResponseJson = requests.get(item.country, headers=headers, timeout=10).json().get("code")
                # playerResponseJson = requests.get(item.id, headers=headers, timeout=10).json().get("player_id")

                put_item_result = table.put_item(Item={
                    "hash_key": f"{gameMode}#{5}",
                    "range_key": f"{item.rank}#{5}",
                    "player_id": f"{5}",
                    "url": f"{item.url}",
                    "username": f"{item.username}",
                    "score": f"{item.score}",
                    "rank": f"{item.rank}",
                    "country": f"{item.country}",
                    "name": f"{item.name}",
                    "status": f"{item.status}",
                    "avatar": f"{item.avatar}",
                    "flair_code": f"{item.flair_code}",
                    "win_count": f"{item.win_count}",
                    "loss_count": f"{item.loss_count}",
                    "draw_count": f"{item.draw_count}"
                })

                print(f"Put item result: {put_item_result}")

            except Exception as e:
                print(f"An error occurred for {item.username}: {e}")


def lambda_handler(event, context):
    playerGameModeHash = fetch_chess_data()
    store_players_to_dynamo(playerGameModeHash)
    return {
        'statusCode': 200,
        'body': json.dumps('Finished updating chess leaderboard data!')
    }