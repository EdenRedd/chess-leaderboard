import boto3
import json
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

table = dynamodb.Table("leaderboard-table")

#CODING ASSIGNMENT: Implement the following two functions

#def create_snapshot():
    #Declare the resources

    # Collect all items (handling pagination)
    # do it with a while loop

    # Optional: add metadata
    # add some metadata like timestamp

    #return snapshot_data

#def upload_snapshot_to_s3(bucket_name, snapshot_data):
    #Create object that you will store
    #crete a timestamp for the file name
    #create the file name/key

    #put the object in s3
    

    # print(f"✅ Snapshot uploaded to s3://{bucket_name}/{file_name}")
    # return file_name