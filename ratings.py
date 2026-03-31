def rate(game_data, game_to_rate, rating):
    for game in game_data:
        if game["name"] == game_to_rate:
            game["rating"] = rating
            return

def rate_all(game_data, ignore_already_rated = True):
    for game in game_data:
        if game["rating"] != -1 and ignore_already_rated:
            continue
        rating = input(f"Type a rating out of 10 for {game['name']}, 'n' to keep unrated, or 'q' to quit: ")
        if rating == "n":
            continue
        elif rating == "q":
            print("Stored previous ratings in local memory, type 'save' to write to file, stopping rating")
            break
        try:
            rating = float(rating)
            game["rating"] = rating
        except ValueError:
            print("Sorry, that's not a number. We'll move on but you can rate again later with the 'rate' command")

def sort_by_rating(game_data, min_rating = 0, print_ratings = True):
    ratings = {10: [], 8: [], 6: [], 4: [], 2: [], 0: [], -1: []}
    for game in game_data:
        if game["rating"] >= 10:
            ratings[10].append(game)
        elif game["rating"] >= 8:
            ratings[8].append(game)
        elif game["rating"] >= 6:
            ratings[6].append(game)
        elif game["rating"] >= 4:
            ratings[4].append(game)
        elif game["rating"] >= 2:
            ratings[2].append(game)
        elif game["rating"] >= 0:
            ratings[0].append(game)
        else:
            ratings[-1].append(game)
    time_to_break = False
    if print_ratings:
        for rating in ratings:
            sorted_ratings = sorted(ratings[rating], key = lambda i: i["rating"], reverse = True)
            print("Games with rating greater than or equal to " + str(rating) + "/10:")
            for game in sorted_ratings:
                if game['rating'] < min_rating:
                    time_to_break = True
                    break
                print(f"-{game['name']}: {game['rating']}")
            if time_to_break:
                break
    return ratings
