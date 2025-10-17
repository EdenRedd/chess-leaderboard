#from chess_leaderboard.services import leaderboard
import boto3
import json
import sys
from services.reader import *


def main():
    snapshot = create_snapshot()
    upload_snapshot_to_s3(snapshot)

if __name__ == "__main__":
    main()

