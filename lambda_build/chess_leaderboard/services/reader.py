import boto3
import json
from datetime import datetime
from boto3.dynamodb.types import TypeDeserializer
from decimal import Decimal
from datetime import datetime, timezone

def retrieve_snapshot_from_s3(snapshot_timestamp= None):
    s3 = boto3.client('s3')
    try:
        if not snapshot_timestamp:
            # Get the latest snapshot if no timestamp is provided
            response = s3.list_objects_v2(Bucket='leaderboard-snapshots')
            all_snapshots = response.get('Contents', [])
            if not all_snapshots:
                print("No snapshots found in the bucket.")
                return None
            latest_snapshot = max(all_snapshots, key=lambda x: x['LastModified'])
            snapshot_timestamp = latest_snapshot['Key']
        obj = s3.get_object(Bucket='leaderboard-snapshots', Key=snapshot_timestamp)
        snapshot_data = json.loads(obj['Body'].read().decode('utf-8'))
        return snapshot_data
    except Exception as e:
        print(f"Error retrieving snapshot: {e}")
        return None

def filter_snapshot(snapshot_data, min_rating=None, max_rating=None, country=None):
    filtered_data = {}
    for mode, players in snapshot_data.items():
        filtered_players = []
        for player in players:
            if min_rating and player.get('rating', 0) < min_rating:
                continue
            if max_rating and player.get('rating', 0) > max_rating:
                continue
            if country and player.get('country', '').lower() != country.lower():
                continue
            filtered_players.append(player)
        filtered_data[mode] = filtered_players
    return filtered_data
    
def lambda_handler(event, context):
    #Check if it is given a timestamp to retrieve a specific snapshot
    #If not get the latest snapshot
    #run the snapshot through the given filters
    #return the filtered snapshot

    timestamp = event.get("queryStringParameters", {}).get("timestamp")
    snapshot_data = retrieve_snapshot_from_s3(timestamp)
    filtered_data = filter_snapshot(snapshot_data, min_rating=1500, country="US")
    print(filtered_data)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(snapshot_data)
    }