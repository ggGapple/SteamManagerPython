import time

import requests
import json
from config import apiKey, mySteamName
import os

def get_player_summary(steamid):
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {"key": apiKey, "steamids": steamid}
    r = requests.get(url, params=params)
    return r.json()["response"]["players"]

def get_id_from_name(username):
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {"key": apiKey, "vanityurl": username}
    r = requests.get(url, params=params)
    data = r.json()["response"]
    if data["success"] == 1:
        return data["steamid"]
    return None

def get_games(mysteamid):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": apiKey,
        "steamid": mysteamid,
        "include_appinfo": True,
        "include_played_free_games": True
    }
    r = requests.get(url, params=params)
    return r.json()["response"]["games"]

def get_data():
    game_data = get_games(mysteamid=mySteamId)
    game_data.sort(key=lambda game: game["playtime_forever"], reverse = True)
    initialize(game_data)
    print("Data obtained")
    return game_data

def get_data_from_config(game_data):
    if os.path.exists("games.json"):
        with open("games.json", "r") as f:
            game_data = json.load(f)
            print("Games retrieved from games.json")

def display(game_data):
    for game in game_data:
        if game["rating"] == -1:
            rating = "unrated"
        else:
            rating = f"rated {game["rating"]} out of 10"
        if len(game["groups"]) > 0:
            in_groups = ", in group(s) "
            for item in game["groups"]:
                in_groups += item + ", "
            in_groups = in_groups[:-2]
        else:
            in_groups = ""
        if len(game["tags"]) > 0:
            tags = ", tags: "
            for item in game['tags']:
                tags += item + ', '
            tags = tags[:-2]
        else:
            tags = ""
        print(f"{BOLD}{game["name"]}:{RESET} {game["playtime_forever"]} mins playtime, " + rating +
              in_groups + tags)

def write():
    if not games:
        print("There are no games stored in local memory. Run getData to get the games data")
        return
    with open("games.json", "w") as f:
        json.dump(games, f, indent=2)
    print("Saved")

def add(game_data, name, playtime):
    game_data.append({"name": name, "playtime_forever": playtime, "rating": -1, "groups": [], "appid": None})
    print("Added " + name + " to data, run write to upload")

def edit_playtime(game_data, name, playtime):
    for game in game_data:
        if game["name"].lower() == name.lower():
            game["playtime_forever"] = playtime
            print("Edited " + name + " in data, run write to upload")
            break
    print("Could not find " + name + " in data")

def edit_name(game_data, name, new_name):
    for game in game_data:
        if game["name"].lower() == name.lower():
            game["name"] = new_name
            print("Edited " + name + " to " + new_name + " in data, run write to upload")
            return
    print("Could not find " + name + " in data")

def remove(game_data, name):
    game_data[:] = [g for g in game_data if g["name"].lower() != name.lower()]
    print("Removed " + name + " from data, run write to upload")

def find(game_data, name):
    for game in game_data:
        if game["name"].lower() == name.lower():
            return True
    return False

def initialize(game_data):
    for game in game_data:
        game["rating"] = -1
        game["groups"] = []
        game['tags'] = []

def rate(game_data, game_to_rate, rating):
    for game in game_data:
        if game["name"] == game_to_rate:
            game["rating"] = rating
            return

def rate_all(game_data, ignore_already_rated = True):
    for game in game_data:
        if game["rating"] != -1 and ignore_already_rated:
            continue
        rating = input(f"Type a rating out of 10 for {game['name']}, 'none' to keep unrated, or 'q' to quit: ")
        if rating == "none":
            continue
        elif rating == "q":
            print("Saved previous ratings, stopping rating")
            break
        try:
            rating = float(rating)
            game["rating"] = rating
        except ValueError:
            print("Sorry, that's not a number. We'll move on but you can rate again later with the 'rate' command")

def del_group(game_data, group_name):
    for game in game_data:
        if group_name in game["groups"]:
            game["groups"].remove(group_name)
    groups.pop(group_name)
    print("Removed " + group_name + " from data, run write to upload")

def del_game_from_group(game_data, game_name, group):
    hit = False
    for game in game_data:
        if game['name'] == game_name:
            hit = True
            if group not in game['groups']:
                print(game + " was never in " + group)
            else:
                game['groups'].remove(group)
                groups[group].remove(game)
                print("Successfully removed " + game + " from "+ group)
    if not hit:
        print("Sorry, that's not a game name")

def add_game_to_group(game_data, game_name, group):
    hit = False
    for game in game_data:
        if game['name'] == game_name:
            hit = True
            if group in game['groups']:
                print(game + " is already in " + group)
            else:
                game['groups'].append(group)
                groups[group].append(game['name'])
                print("Successfully added " + game_name + " to "+ group)
    if not hit:
        print("Sorry, that's not a game name")

def print_members_of_group(group_name):
    print("Members of " + group_name + ":")
    for item in groups[group_name]:
        for thing in item:
            print(thing)


def get_player_achievements(app_id, api_key, steam_id):
    url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {
        "key": api_key,
        "steamid": steam_id,
        "appid": app_id
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    playerstats = data.get("playerstats", {})

    if not playerstats.get("success"):
        return None

    return playerstats.get("achievements", [])

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

games = []
groups = {}
BOLD = "\033[1m"
RESET = "\033[0m"
mySteamId = get_id_from_name(mySteamName)
print("SteamManager v0.2.1\nType 'help' for a list of commands")
if mySteamId is None:
   print("\nWarning: no Steam ID was assigned. Check config.json or make one with 'config' command")
if os.path.exists("games.json"):
    with open("games.json", "r") as f:
        games = json.load(f)
        print("Games retrieved from games.json")
else:
    print("Warning: no data retrieved from games.json. Try uploading data with 'write' command after running 'getData'")

while True:
    command = input("-")
    if command.lower() == "help":
        print("Commands: \n>config: creates a config file based on given Steam key and ID\n"+
              ">getDataFromSteam: read all of the Steam data to a memory\n"+
              ">getDataFromConfig: if a config file exists, read all data from it to a memory\n" +
              ">write: writes the data to a file (resets the file)\n"+
              ">display: prints the data\n"+
              ">add: adds a game to the data\n"+
              ">remove: removes a game from the data\n"+
              ">edit: edits a game's playtime or name\n"+
              ">rate: allows you to add a rating for a game\n"+
              ">rateAll: goes through all games in local memory and asks for a rating\n"+
              ">group: allows you to create/delete/edit groups\n" +
              ">help: prints a list of commands\n"+
              ">updateTags: updates all of the tags ('played,' 'unplayed,' '100%' from Steam data." +
              " Warning: due to Steam requests throttling, this could take a while \n"
              ">quit: quits the program")
    elif command.lower() == "getdatafromsteam":
        games = get_data()
    elif command.lower() == "write":
        write()
    elif command.lower() == "display":
        display(games)
    elif command.lower() == "getdatafromconfig":
        get_data_from_config(games)
    elif command.lower() == "updatetags":
        update_tags(games, apiKey, mySteamId)
    elif command.lower() == "remove":
        removeWhat = input("Type the name of the game to remove: ")
        if not find(games, removeWhat):
            print("Couldn't find " + removeWhat + " in local game data in memory")
            continue
        remove(games, removeWhat)
    elif command.lower() == "edit":
        editMode = input("Would you like to edit a game's playtime or name? Type 'playtime' or 'name': ")
        if editMode.lower() != "playtime" and editMode.lower() != "name":
            print("Sorry, that's an unrecognized command")
            continue
        editWhat = input("Type the name of the game to edit: ")
        if not find(games, editWhat):
            print("Couldn't find " + editWhat + " in local game data in memory")
            continue
        if editMode.lower() == "name":
            whatName = input("Type the new name for the game: ")
            edit_name(games,editWhat,whatName)
            continue
        whatPlaytime = input("Type 'm' to input new playtime in minutes, or 'h' for"+
                             " playtime in hours. Otherwise, the operation will be cancelled: ")
        if whatPlaytime.lower() == "m":
            whatPlaytime = input("Type playtime in minutes: ")
            try:
                whatPlaytime = str(float(whatPlaytime))
            except ValueError:
                print("Sorry, that's not a number")
        elif whatPlaytime.lower() == "h":
            whatPlaytime = input("Type playtime in hours: ")
            try:
                whatPlaytime = float(whatPlaytime)
            except ValueError:
                print("Sorry, that's not a number")
            whatPlaytime = str(whatPlaytime*60)
        else:
            continue
        edit_playtime(games, editWhat, whatPlaytime)
    elif command.lower() == "add":
        addWhat = input("Type the name of the game to add: ")
        whatPlaytime = input("Would you like to input playtime? Type 'm' for playtime in minutes, 'h' for"+
                             " playtime in hours, or 'n' for no playtime: ")
        if whatPlaytime.lower() == "m":
            whatPlaytime = input("Type playtime in minutes: ")
        elif whatPlaytime.lower() == "h":
            whatPlaytime = input("Type playtime in hours: ")
            whatPlaytime =str(float(whatPlaytime)*60)
        else:
            whatPlaytime = 0
        add(games, addWhat, whatPlaytime)
    elif command.lower() == "config":
        apiKey = input("Type your API Key (obtainable here: https://steamcommunity.com/dev/apikey) or 'stop' to exit: ")
        if apiKey.lower() == "stop":
            continue
        keyOrName = input("Do you have a vanity Steam ID? That is, when you view your profile on a browser, "
                          +"in the url is it .com/id/<some number> or .com/id/<some String>? Type 'id' if it's "+
                          "a number, 'name' if it's a String, or 'stop' to quit: ")
        if keyOrName.lower() == "stop":
            continue
        if keyOrName.lower() == "id":
            steamid = input("Type your SteamID: ")
        elif keyOrName.lower() == "name":
            steamid = get_id_from_name(input("Type your Steam vanity name: "))
    elif command.lower() == "rate":
        rateWhat = input("Type the name of the game to rate: ")
        if not find(games, rateWhat):
            print("Couldn't find " + rateWhat + " in local game data in memory")
            continue
        newRating = input("Type the new rating for the game: ")
        rate(games,rateWhat,newRating)
        print(f"Changed rating of {rateWhat} to {newRating}")
    elif command.lower() == "rateall":
        ignoreRating = input("Would you like to ignore already rated games? Type 'y' or 'n': ")
        if ignoreRating.lower() == "y":
            rate_all(games)
        elif ignoreRating.lower() == "n":
            rate_all(games,False)
        else:
            print("Sorry, that's not a recognized command")
    elif command.lower() == "group":
        doWhat = input("Do you want to create a group, delete a group, print a group, or edit members? "
                       +"Type 'create', 'delete', 'print', or 'edit': ")
        if doWhat.lower() == "create":
            groupName = input("What do you want to call this group? ")
            groups[groupName] = []
            print("Created group "+groupName+", enter 'group' command again to add to it")
        elif doWhat.lower() == "delete":
            print("The current groups are: " + str(list(groups.keys())))
            groupName = input("Which group would you like to delete (or enter anything else to not delete)? ")
            if groupName in groups:
                del_group[groupName]
            else:
                print("Sorry, that's not one of the groups")
        elif doWhat.lower() == "edit":
            addOrRemove = input("Do you want to add games to a group or remove games from a group?"
                                +" Type 'add' or 'remove': ")
            skip = False
            if addOrRemove.lower() == "add":
                print("The current groups are: " + str(list(groups.keys())))
                groupName = input("What group do you want to add to? ")
                if groupName not in groups:
                    print("Sorry, that's not one of the groups")
                else:
                    for i in range(len(games)):
                        gameToAdd = input("Type the name of a game to add or 'stop' to quit: ")
                        if gameToAdd.lower() == "stop":
                            skip = True
                            break
                        add_game_to_group(games,gameToAdd,groupName)
            elif addOrRemove.lower() == "remove":
                print("The current groups are: " + str(list(groups.keys())))
                groupName = input("What group do you want to remove from? ")
                if groupName not in groups:
                    print("Sorry, that's not one of the groups")
                else:
                    for i in range(len(games)):
                        gameToRemove = input("Type the name of a game to remove or 'stop' to quit: ")
                        if gameToRemove.lower() == "stop":
                            skip = True
                            break
                        del_game_from_group(games,gameToRemove,groupName)
            else:
                print("Sorry, that's not a recognized command")
            if skip:
                continue
        elif doWhat.lower() == "print":
            print("The current groups are: " + str(list(groups.keys())))
            whatGroup = input("What group do you want to print? ")
            if whatGroup not in groups:
                print("Sorry, that's not one of the groups")
            else:
                print_members_of_group(whatGroup)
        else:
            print("Sorry, that's not a recognized command")
            continue
    elif command.lower() == "quit":
        print("Exited SteamManager")
        break
    else:
        print("Sorry, that's not a recognized command")