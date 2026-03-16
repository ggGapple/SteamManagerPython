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
    print("data obtained")
    return game_data

def display(game_data):
    for game in game_data:
        print(game["name"], "-", game["playtime_forever"], "mins")

def write():
    if not games:
        print("no games")
        return
    with open("games.json", "w") as f:
        json.dump(games, f, indent=2)
    print("saved")

games = []

mySteamId = get_id_from_name(mySteamName)
print("go")
while True:
    command = input("")
    if command == "getData":
        games = get_data()
    if command == "write":
        write()
    if command == "display":
        display(games)