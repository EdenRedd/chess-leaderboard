import boto3
import json
from datetime import datetime
from boto3.dynamodb.types import TypeDeserializer
from decimal import Decimal
from datetime import datetime, timezone

def retrieve_snapshot_from_s3(snapshot_timestamp= None):
    s3 = boto3.client('s3')
    print("Function called successfully, Running retrieve_snapshot_from_s3")
    all_snapshots = []
    try:
        if not snapshot_timestamp:
            print("Retrieving latest snapshot")
            # Get the latest snapshot if no timestamp is provided
            response = s3.list_objects_v2(Bucket='leaderboard-snapshots')
            all_snapshots.extend(response.get('Contents', []))

            while response.get('IsTruncated'):
                response = s3.list_objects_v2(
                    Bucket='leaderboard-snapshots',
                    ContinuationToken=response['NextContinuationToken']
                )
                all_snapshots.extend(response.get('Contents', []))
            if not all_snapshots:
                print("No snapshots found in the bucket.")
                return None
            latest_snapshot = max(all_snapshots, key=lambda x: x['LastModified'])
            snapshot_timestamp = latest_snapshot['Key']
        print("Retrieved latest snapshot:", snapshot_timestamp)
        obj = s3.get_object(Bucket='leaderboard-snapshots', Key=snapshot_timestamp)
        snapshot_data = json.loads(obj['Body'].read().decode('utf-8'))
        print("Snapshot data retrieved successfully")
        #print(snapshot_data)
        return snapshot_data
    except Exception as e:
        print(f"Error retrieving snapshot: {e}")
        return None

def filter_snapshot(snapshot_data, game_Mode=None, country=None):
    filtered_players = []

    for player in snapshot_data:
        player_country = player.get('GameModeCountryCode', '').split('#')[-1].lower()
        gameMode = player.get('GameModeCountryCode', '').split('#')[0].lower() 

        if country and player_country != country.lower():
            continue
        if game_Mode and gameMode != game_Mode.lower():
            continue

        filtered_players.append(player)

    return filtered_players

import json

def sort_by_rank_desc(data):
    # Sort descending by the numeric portion of "RankAndID"
    sorted_data = sorted(
        data,
        key=lambda item: int(str(item["RankAndID"]).split("#")[0]),
        reverse=False  # False = ascending (1 first), True = descending (highest first)
    )
    return sorted_data


def sort_by_rank_desc(data):
    # Sort descending by the numeric portion of "RankAndID"
    sorted_data = sorted(
        data,
        key=lambda item: int(str(item["RankAndID"]).split("#")[0]),
        reverse=False  # False = ascending (1 first), True = descending (highest first)
    )
    return sorted_data


    
def get_snapshot(event, context):

    #timestamp = event.get("queryStringParameters", {}).get("timestamp")
    params = event.get("queryStringParameters", {})
    country = params["country"] if "country" in params else None
    game_mode = params["game_mode"] if "game_mode" in params else None
    snapshot_data = retrieve_snapshot_from_s3()
    filtered_data = filter_snapshot(snapshot_data, game_Mode=game_mode, country=country)
    sorted_data = sort_by_rank_desc(filtered_data)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(sorted_data)
    }