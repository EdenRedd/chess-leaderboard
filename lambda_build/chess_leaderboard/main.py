#from chess_leaderboard.services import leaderboard
import boto3
import json
import sys


dynamodb = boto3.client('dynamodb')

TABLE_NAME = 'chess-leaderboard-players'

def fetch_entire_table():
    items = []
    response = dynamodb.scan(TableName=TABLE_NAME)
    items.extend(response['Items'])

    # Paginate if there are more items
    while 'LastEvaluatedKey' in response:
        response = dynamodb.scan(
            TableName=TABLE_NAME,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response['Items'])

    print(f"Total items fetched: {len(items)}")
    return items


def main():
    print("Entering main function")
    
    data = fetch_entire_table()

    # (Optional) Convert DynamoDB JSON to normal Python dicts
    from boto3.dynamodb.types import TypeDeserializer
    deserializer = TypeDeserializer()

    plain_data = [
        {k: deserializer.deserialize(v) for k, v in item.items()}
        for item in data
    ]

    # Measure approximate JSON size
    snapshot_json = json.dumps(plain_data, default=lambda o: float(o))
    print(f"Snapshot size: {sys.getsizeof(snapshot_json)/1024:.2f} KB")



    # print("Fetching player data")
    # playerGameModeHash = leaderboard.fetch_chess_data()
    # print("Fetched chess data")
    # leaderboard.store_players_to_dynamo(playerGameModeHash)

if __name__ == "__main__":
    main()

