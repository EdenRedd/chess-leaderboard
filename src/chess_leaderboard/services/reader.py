import boto3
import json
from datetime import datetime
from boto3.dynamodb.types import TypeDeserializer
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

table = dynamodb.Table("leaderboard-table")

#CODING ASSIGNMENT: Implement the following two functions
#3. We need a lambda function that will go to the snapshot and get the info
#4. We need a function that will filter out based on params
####### #3 and #4 we need to implement after this 
def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        # convert to float (or int if you prefer)
        return float(obj)
    else:
        return obj

def create_snapshot():
    dynamodb = boto3.resource('dynamodb')
    leaderboardTable = dynamodb.Table('leaderboard-table')

    entries = []
    response = leaderboardTable.scan()
    entries.extend([convert_decimals(i) for i in response['Items']])

    while 'LastEvaluatedKey' in response:
        response = leaderboardTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        entries.extend([convert_decimals(i) for i in response['Items']])

    print("Successfully retrieved all DynamoDB items")
    return entries

def upload_snapshot_to_s3(snapshot_data):
    s3 = boto3.resource('s3')
    obj = s3.Object('leaderboard-snapshots', 'folder/hello.txt')

    obj.put(Body=json.dumps(snapshot_data),
        ContentType='application/json')