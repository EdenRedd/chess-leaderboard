# import boto3
# import json
# from datetime import datetime

# dynamodb = boto3.resource('dynamodb')
# s3 = boto3.client('s3')

# table = dynamodb.Table("leaderboard-table")

# #CODING ASSIGNMENT: Implement the following two functions

# #We need a couple of things
# #1. Scan the items and put them into an object
# #2. Uploading the file to s3
# ####### THOSE ARE THE 2 I AM ABOUT TO IMPLEMENT#########
# #3. We need a lambda function that will go to the snapshot and get the info
# #4. We need a function that will filter out based on params
# ####### #3 and #4 we need to implement after this 

# def create_snapshot():
#     #Declare the resources
#     snapshot_data = ""
#     # Collect all items (handling pagination)
#     # do it with a while loop

#     # Optional: add metadata
#     # add some metadata like timestamp

#     return snapshot_data

# #def upload_snapshot_to_s3(bucket_name, snapshot_data):
#     #Create object that you will store
#     #crete a timestamp for the file name
#     #create the file name/key

#     #put the object in s3
    

#     # print(f"✅ Snapshot uploaded to s3://{bucket_name}/{file_name}")
#     # return file_name