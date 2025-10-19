#from chess_leaderboard.services import leaderboard
import boto3
import json
import sys
from services.reader import *


def main():
    timestamp = event.get("queryStringParameters", {}).get("timestamp")
    snapshot = retrieve_snapshot_from_s3()
    print(snapshot)

if __name__ == "__main__":
    main()

