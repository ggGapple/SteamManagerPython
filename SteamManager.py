import requests
import json
from config import apiKey, mySteamName

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
    print("Data obtained")
    return game_data

def display(game_data):
    for game in game_data:
        print(game["name"], "-", game["playtime_forever"], "mins")

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

def edit(game_data, name, playtime):
    for game in game_data:
        if game["name"] == name:
            game["playtime_forever"] = playtime
            print("Edited " + name + " in data, run write to upload")
            break
    print("Could not find " + name + " in data")

def remove(game_data, name):
    game_data = [g for g in game_data if g["name"] != name]
    print("Removed " + name + " from data, run write to upload")

games = []
mySteamId = get_id_from_name(mySteamName)
print("SteamManager v0.1\nType 'help' for a list of commands")
if mySteamId is None:
   print("\nWarning: No Steam ID was assigned. Check config.json or make one with 'config' command")
while True:
    command = input("-")
    if command == "help":
        print("Commands: \n>config: creates a config file based on given Steam key and ID\n"+
              ">getData: read all of the Steam data to a memory\n"+
              ">write: writes the data to a file (resets the file)\n"+
              ">display: prints the data\n"+
              ">add: adds a game to the data\n"+
              ">remove: removes a game from the data\n"+
              ">edit: edits a game\n"+
              ">help: prints a list of commands")
    elif command == "getData":
        games = get_data()
    elif command == "write":
        write()
    elif command == "display":
        display(games)
    elif command == "remove":
        removeWhat = input("Type the name of the game to remove: ")
        remove(games, removeWhat)
    elif command == "edit":
        editWhat = input("Type the name of the game to add: ")
        whatPlaytime = input("Would you like to input playtime? Type 'm' for playtime in minutes, 'h' for"+
                             " playtime in hours, or 'n' for no playtime: ")
        if whatPlaytime == "m":
            whatPlaytime = input("Type playtime in minutes: ")
        elif whatPlaytime == "h":
            whatPlaytime = input("Type playtime in hours: ")
            whatPlaytime *= 60
        else:
            whatPlaytime = 0
        edit(games, whatPlaytime, whatPlaytime)
    elif command == "config":
        apiKey = input("Type your API Key (obtainable here: https://steamcommunity.com/dev/apikey): ")
        keyOrName = input("Do you have a vanity Steam ID? That is, when you view your profile on a browser, "
                          +"in the url is it .com/id/<some number> or .com/id/<some String>? Type 'id' if it's "+
                          "a number, or 'name' if it's a String: ")
        if keyOrName == "id":
            steamid = input("Type your SteamID: ")
        elif keyOrName == "name":
            steamid = get_id_from_name(input("Type your Steam vanity name: "))
    else:
        print("Sorry, that's not a recognized command")