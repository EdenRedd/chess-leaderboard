#from chess_leaderboard.services import leaderboard
import boto3
import json
import sys
from services.reader import *
from services.leaderboard import *


def main():
    # playerGameModeHash = fetch_chess_data()
    # store_players_to_dynamo(playerGameModeHash)
    snapshot = create_snapshot()
    #seperate the snapshots into a list of their own game modes
    #Edit the upload function to upload seperate files for the game modes
    upload_snapshot_to_s3(snapshot)

if __name__ == "__main__":
    main()

