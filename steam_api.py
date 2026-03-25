import requests
import json
import os
from config import api_key
from config import steam_name

def get_player_summary(steamid):
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {"key": api_key, "steamids": steamid}
    r = requests.get(url, params=params)
    return r.json()["response"]["players"]

def get_id_from_name(username):
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {"key": api_key, "vanityurl": username}
    r = requests.get(url, params=params)
    data = r.json()["response"]
    if data["success"] == 1:
        return data["steamid"]
    return None

def get_games(mysteamid):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": api_key,
        "steamid": mysteamid,
        "include_appinfo": True,
        "include_played_free_games": True
    }
    r = requests.get(url, params=params)
    return r.json()["response"]["games"]

def get_data():
    steam_id = get_id_from_name(steam_name)
    game_data = get_games(mysteamid=steam_id)
    game_data.sort(key=lambda game: game["playtime_forever"], reverse = True)
    initialize(game_data)
    print("Data obtained")
    return game_data

def initialize(game_data):
    for game in game_data:
        game["rating"] = -1
        game["groups"] = []
        game['tags'] = []
        game['notes'] = ""

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


def get_review_data(app_id):
    url = f"https://store.steampowered.com/appreviews/{app_id}"
    params = {
        "json": 1,
        "language": "all",
        "purchase_type": "all"
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    summary = response.json().get("query_summary", {})
    total = summary.get("total_reviews", 0)
    positive = summary.get("total_positive", 0)

    return {
        "positive": positive,
        "negative": summary.get("total_negative", 0),
        "total": total,
        "score_desc": summary.get("review_score_desc", ""),  # e.g. "Very Positive"
        "positive_pct": round((positive / total) * 100, 2) if total > 0 else 0
    }