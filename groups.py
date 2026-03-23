def del_group(game_data, group_name,groups):
    for game in game_data:
        if group_name in game["groups"]:
            game["groups"].remove(group_name)
    groups.pop(group_name)
    print("Removed " + group_name + " from data, run write to upload")

def del_game_from_group(game_data, game_name, group, groups):
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

def add_game_to_group(game_data, game_name, group, groups):
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

def print_members_of_group(group_name, groups):
    print("Members of " + group_name + ":")
    for item in groups[group_name]:
        for thing in item:
            print(thing)