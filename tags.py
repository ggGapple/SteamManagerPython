import time
from steam_api import get_player_achievements

def update_tags(game_data, api_key, steam_id):
    index = 0;
    for game in game_data:
        print("Updating tags for " + game["name"] + " (" + str(round(index * 100 / len(game_data),2))+"%)")
        index+=1
        if game["playtime_forever"] == 0:
            game['tags'].append("unplayed")
        app_id = game["appid"]
        achievements = get_player_achievements(app_id, api_key, steam_id)

        if achievements is None:
            # no achievements for this game, skip
            time.sleep(0.1)  # still rate limit to be safe
            continue

        total = len(achievements)
        unlocked = sum(1 for a in achievements if a["achieved"] == 1)

        if 0 < total == unlocked:
            if "100%" not in game["tags"]:
                game["tags"].append("100%")

        time.sleep(0.05)  # avoid hitting Steam's rate limit (~2 req/sec)
    print("Updated all tags")