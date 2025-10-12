import boto3
import requests
import json
import sys
from chess_leaderboard.models.player import PlayerData
from pathlib import Path

# --------------------------
# This function fetches all the players on the leaderboard from chess.com
# stores them into an object and returns them in form of a hash map
# where the key is the game mode and the value is a list of players
#
# returns gameModeHash which is a hashmap of game mode keys and list of players for values
# --------------------------
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
        
# --------------------------
# This function takes a hashmap of game modes and list of players
# and stores them into a DynamoDB table
#
# param players: hashmap of game modes and list of players with keys being game modes
# returns gameModeHash which is a hashmap of game mode keys and list of players for values
# --------------------------
def store_players_to_dynamo(players):
    headers = {
        "User-Agent": (
            "chess-leaderboard-demo/0.1 "
            "(https://github.com/yourGitHub; contact: you@example.com)"
        )
    }

    dynamodbService = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodbService.Table('leaderboard-table')

    # Caches to avoid repeated API calls
    country_cache = {}
    player_cache = {}

    print("Starting to store players...")

    for gameMode in players.keys():
        for item in players[gameMode]:
            try:
                # Country caching
                if item.country not in country_cache:
                    response = requests.get(item.country, headers=headers, timeout=10)
                    response.raise_for_status()
                    country_cache[item.country] = response.json().get("code")

                country_code = country_cache[item.country]

                # Player ID caching
                if item.id not in player_cache:
                    response = requests.get(item.id, headers=headers, timeout=10)
                    response.raise_for_status()
                    player_cache[item.id] = response.json().get("player_id")

                player_id = player_cache[item.id]

                # Store in DynamoDB
                put_item_result = table.put_item(Item={
                    "GameModeCountryCode": f"{gameMode}#{country_code}",
                    "RankAndID": f"{item.rank}#{player_id}",
                    "player_id": player_id,
                    "url": item.url,
                    "username": item.username,
                    "score": item.score,
                    "rank": item.rank,
                    "country": item.country,
                    "name": item.name,
                    "status": item.status,
                    "avatar": item.avatar,
                    "flair_code": item.flair_code,
                    "win_count": item.win_count,
                    "loss_count": item.loss_count,
                    "draw_count": item.draw_count
                })

                print(f"Stored {item.username} (rank {item.rank}) → {put_item_result}")

            except Exception as e:
                print(f"An error occurred for {item.username}: {e}")

# --------------------------
# This lambda handler function is the entry point for AWS Lambda
# this particular lambda handler contains the logic to fetch the chess API leaderboard data
# and stores it into DynamoDB
# --------------------------
def lambda_handler(event, context):
    playerGameModeHash = fetch_chess_data()
    store_players_to_dynamo(playerGameModeHash)
    return {
        'statusCode': 200,
        'body': json.dumps('Finished updating chess leaderboard data!')
    }