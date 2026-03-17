import requests
import json
from config import apiKey, mySteamName
import os

def get_player_summary(steamid):
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {"key": apiKey, "steamids": steamid}
    r = requests.get(url, params=params)
    return r.json()["response"]["players"]

def get_id_from_name(username):
    url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {"key": apiKey, "vanityurl": username}
    r = requests.get(url, params=params)
    data = r.json()["response"]
    if data["success"] == 1:
        return data["steamid"]
    return None

def get_games(steamid):
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": apiKey,
        "steamid": steamid,
        "include_appinfo": True,
        "include_played_free_games": True
    }
    r = requests.get(url, params=params)
    return r.json()["response"]["games"]

def get_data():
    game_data = get_games(steamid=mySteamId)
    game_data.sort(key=lambda game: game["playtime_forever"], reverse = True)
    initialize_ratings(game_data)
    print("Data obtained")
    return game_data

def display(game_data):
    for game in game_data:
        if game["rating"] == -1:
            print(f"{BOLD}{game["name"]}:{RESET} {game["playtime_forever"]} mins playtime, unrated")
        else:
            print(f"{BOLD}{game["name"]}:{RESET} {game["playtime_forever"]} mins playtime, rated {game["rating"]} out of 10")

def write():
    if not games:
        print("There are no games stored in local memory. Run getData to get the games data")
        return
    with open("games.json", "w") as f:
        json.dump(games, f, indent=2)
    print("Saved")

def add(game_data, name, playtime):
    game_data.append({"name": name, "playtime_forever": playtime, "appid": None})
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

def initialize_ratings(game_data):
    for game in game_data:
        game["rating"] = -1

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

games = []
BOLD = "\033[1m"
RESET = "\033[0m"
mySteamId = get_id_from_name(mySteamName)
print("SteamManager v0.1\nType 'help' for a list of commands")
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
              ">getData: read all of the Steam data to a memory\n"+
              ">write: writes the data to a file (resets the file)\n"+
              ">display: prints the data\n"+
              ">add: adds a game to the data\n"+
              ">remove: removes a game from the data\n"+
              ">edit: edits a game's playtime or name\n"+
              ">rate: allows you to add a rating for a game\n"+
              ">rateAll: goes through all games in local memory and asks for a rating\n"+
              ">help: prints a list of commands\n"+
              ">quit: quits the program")
    elif command.lower() == "getdata" or command.lower() == "get data":
        games = get_data()
    elif command.lower() == "write":
        write()
    elif command.lower() == "display":
        display(games)
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
        apiKey = input("Type your API Key (obtainable here: https://steamcommunity.com/dev/apikey): ")
        keyOrName = input("Do you have a vanity Steam ID? That is, when you view your profile on a browser, "
                          +"in the url is it .com/id/<some number> or .com/id/<some String>? Type 'id' if it's "+
                          "a number, or 'name' if it's a String: ")
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
            print("Sorry, that's not a unrecognized command")
    elif command.lower() == "quit":
        break
    else:
        print("Sorry, that's not a recognized command")