# Chess Leaderboard API Design

## Internal (System-Only Endpoints)

| Method | Endpoint     | Description                                                     |
| ------ | ------------ | --------------------------------------------------------------- |
| POST   | /player      | Creates new players based on Chess.com’s API into the database. |
| PUT    | /player/{id} | Updates information about an existing player.                   |
| DELETE | /player/{id} | Removes a player from the database.                             |
| POST   | /match       | Creates a new match in the database.                            |
| PUT    | /match/{id}  | Updates a specific match result.                                |
| DELETE | /match/{id}  | Deletes a specified match from the database.                    |

---

## External (Public Endpoints)

| Method | Endpoint              | Description                                  |
| ------ | --------------------- | -------------------------------------------- |
| GET    | /leaderboard          | Fetches the top players.                     |
| GET    | /players              | Retrieves information for all players.       |
| GET    | /player/{id}          | Retrieves information for a specific player. |
| GET    | /matches              | Retrieves a list of recorded games.          |
| GET    | /match/{id}           | Retrieves a specific game match result.      |
| GET    | /players/{id}/matches | Retrieves matches played by a single player. |
