import os
import json

def write(game_data, groups):
    if not game_data:
        print("No games in memory to save. Run load first")
        return
    with open("games.json", "w") as f:
        json.dump({"games": game_data, "groups": groups}, f, indent=2)
    print("Saved")

def load_from_file():
    if os.path.exists("games.json"):
        with open("games.json", "r") as f:
            data = json.load(f)
            games = data.get("games", [])
            groups = data.get("groups", {})
            for game in games:
                game.setdefault("tags", [])
                game.setdefault("notes", "")
                game.setdefault("groups", [])
            print("Games retrieved from games.json")
            return games, groups
    else:
        print("No games.json file found")
        return [], {}