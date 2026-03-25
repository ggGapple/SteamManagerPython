BOLD = "\033[1m"
RESET = "\033[0m"

def display(game_data):
    for game in game_data:
        display_game_knowing_id(game_data,game)

def display_game(game_data, game_name):
    for potential_game in game_data:
        if potential_game["name"] != game_name:
            continue
        display_game_knowing_id(game_data,potential_game)

def display_game_knowing_id(game_data, game):
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
    notes = ", notes: " + game['notes']
    print(f"{BOLD}{game["name"]}:{RESET} {game["playtime_forever"]} mins playtime, " + rating +
          in_groups + tags + notes)

def add(game_data, name, playtime, rating=-1, notes=""):
    game_data.append({"name": name, "playtime_forever": playtime, "rating": rating,
                      "groups": [], "appid": None, "tags": [], "notes": notes})
    print("Added " + name + " to data, run save to upload")

def edit_playtime(game_data, name, playtime):
    for game in game_data:
        if game["name"].lower() == name.lower():
            game["playtime_forever"] = playtime
            print("Edited " + name + " in data, run save to upload")
            return
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