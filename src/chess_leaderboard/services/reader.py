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

def filter_snapshot(snapshot_data, min_rating=None, max_rating=None, country=None):
    filtered_players = []

    for player in snapshot_data:
        rating = player.get('score', 0)  # looks like your JSON uses 'score' not 'rating'
        player_country = player.get('country', '').split('/')[-1].lower()  # extract 'PH' from URL

        if min_rating is not None and rating < min_rating:
            continue
        if max_rating is not None and rating > max_rating:
            continue
        if country and player_country != country.lower():
            continue

        filtered_players.append(player)

    return filtered_players

    
def get_snapshot(event, context):
    #Check if it is given a timestamp to retrieve a specific snapshot
    #If not get the latest snapshot
    #run the snapshot through the given filters
    #return the filtered snapshot

    #timestamp = event.get("queryStringParameters", {}).get("timestamp")
    snapshot_data = retrieve_snapshot_from_s3()
    filtered_data = filter_snapshot(snapshot_data, min_rating=1500, country="US")
    print(filtered_data)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(snapshot_data)
    }