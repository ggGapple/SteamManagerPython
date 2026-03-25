import random
def recommend_random(game_data):
    return random.choice(game_data)

def recommend(game_data, rating_min = -1, rating_max = -1, tag = None, group = None):
    potential_games = []
    rating_check = rating_min != -1
    rating_check_w_max = rating_max != -1 and rating_check
    tag_check = tag is not None
    group_check = group is not None
    for game in game_data:
        if rating_check:
            if game["rating"] < rating_min:
                continue
        if rating_check_w_max:
            if game["rating"] > rating_max:
                continue
        if tag_check:
            if tag not in game["tags"]:
                continue
        if group_check:
            if group not in game["groups"]:
                continue
        potential_games.append(game)
    return random.choice(potential_games)