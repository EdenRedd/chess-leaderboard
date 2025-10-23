#from chess_leaderboard.services import leaderboard
import boto3
import json
import sys
from services.reader import *


def main():
    snapshot = retrieve_snapshot_from_s3()
    #filtered_data = filter_snapshot(snapshot, min_rating=902742.0, country="US")
    #print(filtered_data)

if __name__ == "__main__":
    main()

