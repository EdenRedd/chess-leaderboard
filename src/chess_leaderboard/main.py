from chess_leaderboard.services import leaderboard

def main():
    print("Entering main function")
    players = leaderboard.fetch_chess_data()
    print(players)
    #leaderboard.store_players_to_dynamo(players)

    if __name__ == "__main__":
        main()