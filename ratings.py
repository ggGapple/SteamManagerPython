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
