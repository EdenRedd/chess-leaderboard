from chess_leaderboard.services import leaderboard

def main():
    print("Entering main function")
    playerGameModeHash = leaderboard.fetch_chess_data()
    print("Fetched chess data")
    leaderboard.store_players_to_dynamo(playerGameModeHash)

    if __name__ == "__main__":
        main()