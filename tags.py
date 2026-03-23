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

        if achievements is None or app_id is None:
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

def add_tag(game_data, game_name, tag):
    for game in game_data:
        if game["name"] == game_name:
            game["tags"].append(tag)
            print("Added tag " + tag + " to " + game_name)
            return
    print("Could not find " + game_name + " in data")

def clear_tags(game_data, game_name):
    for game in game_data:
        if game["name"] == game_name:
            game["tags"] = []
            print("Cleared tags for " + game_name)
            return
    print("Could not find " + game_name + " in data")

def remove_tag_from_game(game_data, game_name, tag_name):
    for game in game_data:
        if game["name"] == game_name:
            if tag_name not in game["tags"]:
                print(game_name + " does not have tag " + tag_name)
                return
            game["tags"].remove(tag_name)
            print("Removed tag " + tag_name + ' from ' + game_name)

def delete_tag(game_data, tag_name):
    for game in game_data:
        if tag_name in game["tags"]:
            game["tags"].remove(tag_name)
            print("Removed tag " + tag_name + ' from ' + game["name"])
    print("Removed tag " + tag_name + ' from all games')

def print_tags(game_data, game_name):
    to_print = game_name + " has tags "
    for game in game_data:
        if game["name"] == game_name:
            for tag in game["tags"]:
                to_print += tag+", "
            print(to_print[0:-2])
            return
    print("Could not find " + game_name + " in data")

def print_games_of_tag(game_data, tag_name):
    print("Printing games of " + tag_name)
    for game in game_data:
        if tag_name in game["tags"]:
            print(game["name"])

def print_all_tags(game_data):
    print("Printing all tags")
    tags_list = []
    for game in game_data:
        for tag in game["tags"]:
            if tag not in tags_list:
                tags_list.append(tag)
                print(tag)