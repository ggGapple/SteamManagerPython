def add_notes(game_data, game_name, notes):
    for game in game_data:
        if game["name"] == game_name:
            game["notes"] = notes
            print("Updated " + game_name + " notes to " + notes)
            return