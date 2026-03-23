from config import api_key, steam_name
from steam_api import *
from tags import *
from groups import *
from game_utils import *
from notes import *
from ratings import *
from storage import *
BOLD = "\033[1m"
RESET = "\033[0m"

games = []
groups = {}
steam_id = get_id_from_name(steam_name)
print("SteamManager v0.3.2\nType 'help' for a list of commands")
if steam_id is None:
   print("\nWarning: no Steam ID was assigned. Check config.json or make one with 'config' command")
if os.path.exists("games.json"):
    games, groups = load_from_file()
else:
    print("Warning: no data retrieved from games.json. Try uploading data with 'write' command after running 'getData'")

while True:
    command = input("-")
    if command.lower() == "help":
         print("Commands:\n"
              ">load: load games from 'steam' or 'file'\n"
              ">save: save current data to file\n"
              ">display: print all games\n"
              ">add: add a game (prompts for playtime, rating, notes)\n"
              ">remove: remove a game\n"
              ">edit: edit a game's name, playtime, or notes\n"
              ">rate: rate a game (or all at once)\n"
              ">tags: update/configure tags\n"
              ">group: create/delete/edit/print groups\n"
              ">help: show this list\n"
              ">quit: exit the program")


    elif command.lower() == "load":
        source = input("Load from 'steam' or 'file'? ")
        if source.lower() == "steam":
            games = get_data()
        elif source.lower() == "file":
            games, groups = load_from_file()
        else:
            print("Sorry, that's not a recognized source")


    elif command.lower() == "save":
        write(games, groups)


    elif command.lower() == "display":
        display(games)


    elif command.lower() == "tags":
        do_what = input("Do you want to update all tags from steam data (warning: can take a while), "
                        +"add a tag to games, remove tags from games, or print certain games with certain tags?"
                        +" Type 'update', 'add', 'remove', or 'print': ")
        if do_what.lower() == "update":
            update_tags(games, api_key, steam_id)
        elif do_what.lower() == "add":
            tag_name = input("What tag would you like to add? ")
            for i in range(len(games)):
                what_game = input("Type a game to add the tag to, or type 'stop' to quit: ")
                if what_game.lower() == "stop":
                    break
                add_tag(games, what_game, tag_name)
        elif do_what.lower() == "remove":
            remove_how = input("Do you want to clear a game of all its tags, clear a tag from all games, "
                               +"or remove a specific tag from a specific game? " +
                                "Type 'game', 'tag', or 'specific': ")
            if remove_how.lower() == "game":
                what_game = input("What game would you like to clear all the tags from? ")
                clear_tags(games,what_game)
            elif remove_how.lower() == "tag":
                what_tag = input("What tag would you like to clear from all games? ")
                delete_tag(games,what_tag)
            elif remove_how.lower() == "specific":
                what_game = input("What game would you like to clear a tag from? ")
                print_tags(games,what_game)
                what_tag = input("What tag would you like to remove from "+what_game+"? ")
                remove_tag_from_game(games,what_game,what_tag)
            else:
                print("Sorry, that's not a recognized command")
        elif do_what.lower() == "print":
            print_what = input("Do you want to print all all tags, all tags on a certain game, "
                               +"or all the games with a certain tag? "
                               +"Type 'all', 'game', or 'tags': ")
            if print_what.lower() == 'game':
                what_game = input("What game do you want to print all the tags on? ")
                print_tags(games,what_game)
            elif print_what.lower() == 'tags':
                what_tag = input("What tag do you want to print all the games of? ")
                print_games_of_tag(games, what_tag)
            elif print_what.lower() == 'all':
                print_all_tags(games)
            else:
                print("Sorry, that's not a recognized command")
        else:
            print("Sorry, that's not a recognized command")

    elif command.lower() == "remove":
        removeWhat = input("Type the name of the game to remove: ")
        if not find(games, removeWhat):
            print("Couldn't find " + removeWhat + " in local game data in memory")
            continue
        remove(games, removeWhat)


    elif command.lower() == "edit":
        editWhat = input("Type the name of the game to edit: ")
        if not find(games, editWhat):
            print("Couldn't find " + editWhat + " in local game data in memory")
            continue
        editMode = input("What would you like to edit? Type 'name', 'playtime', or 'notes': ")
        if editMode.lower() == "name":
            whatName = input("Type the new name: ")
            edit_name(games, editWhat, whatName)
        elif editMode.lower() == "playtime":
            whatPlaytime = input("Type playtime in minutes or hours (e.g. '90m' or '2h'): ")
            if whatPlaytime.lower().endswith("m"):
                try:
                    edit_playtime(games, editWhat, float(whatPlaytime[:-1]))
                except ValueError:
                    print("Sorry, that's not a valid number")
            elif whatPlaytime.lower().endswith("h"):
                try:
                    edit_playtime(games, editWhat, float(whatPlaytime[:-1]) * 60)
                except ValueError:
                    print("Sorry, that's not a valid number")
            else:
                print("Sorry, that's not a recognized format")
        elif editMode.lower() == "notes":
            whatNotes = input("Type the new notes: ")
            add_notes(games, editWhat, whatNotes)
        else:
            print("Sorry, that's not a recognized command")


    elif command.lower() == "add":
        addWhat = input("Type the name of the game to add: ")
        whatPlaytime = input("Type playtime in minutes, hours, or 'n' for none (e.g. '90m' or '2h'): ")
        if whatPlaytime.lower() == "n":
            playtime = 0
        elif whatPlaytime.lower().endswith("m"):
            try:
                playtime = float(whatPlaytime[:-1])
            except ValueError:
                print("Sorry, that's not a valid number")
                continue
        elif whatPlaytime.lower().endswith("h"):
            try:
                playtime = float(whatPlaytime[:-1]) * 60
            except ValueError:
                print("Sorry, that's not a valid number")
                continue
        else:
            print("Sorry, that's not a recognized format")
            continue
        newRating = input(f"Type a rating out of 10 for {addWhat}, or 'n' to skip: ")
        rating = -1
        if newRating.lower() != "n":
            try:
                rating = float(newRating)
            except ValueError:
                print("Sorry, that's not a number, game will be added as unrated")
        whatNotes = input("Type any notes, or 'n' to skip: ")
        notes = "" if whatNotes.lower() == "n" else whatNotes
        add(games, addWhat, playtime, rating, notes)


    elif command.lower() == "config":
        api_key = input("Type your API Key (obtainable here: https://steamcommunity.com/dev/api_key) or 'stop' to exit: ")
        if api_key.lower() == "stop":
            continue
        keyOrName = input("Do you have a vanity Steam ID? That is, when you view your profile on a browser, "
                          +"in the url is it .com/id/<some number> or .com/id/<some String>? Type 'id' if it's "+
                          "a number, 'name' if it's a String, or 'stop' to quit: ")
        if keyOrName.lower() == "stop":
            continue
        if keyOrName.lower() == "id":
            steamid = input("Type your SteamID: ")
        elif keyOrName.lower() == "name":
            steamid = get_id_from_name(input("Type your Steam vanity name: "))


    elif command.lower() == "rate":
        allOrOne = input("Would you like to rate all games at once or a single game? Type 'all' or 'one': ")
        if allOrOne.lower() == "all":
            ignoreRating = input("Would you like to ignore already rated games? Type 'y' or 'n': ")
            if ignoreRating.lower() == "y":
                rate_all(games)
            elif ignoreRating.lower() == "n":
                rate_all(games, False)
            else:
                print("Sorry, that's not a recognized command")
        elif allOrOne.lower() == "one":
            rateWhat = input("Type the name of the game to rate: ")
            if not find(games, rateWhat):
                print("Couldn't find " + rateWhat + " in local game data in memory")
                continue
            newRating = input("Type the new rating for the game: ")
            rate(games, rateWhat, newRating)
            print(f"Changed rating of {rateWhat} to {newRating}")
        else:
            print("Sorry, that's not a recognized command")


    elif command.lower() == "group":
        doWhat = input("Do you want to create a group, delete a group, print a group, or edit members? "
                       +"Type 'create', 'delete', 'print', or 'edit': ")
        if doWhat.lower() == "create":
            groupName = input("What do you want to call this group? ")
            groups[groupName] = []
            print("Created group "+groupName+", enter 'group' command again to add to it")
        elif doWhat.lower() == "delete":
            print("The current groups are: " + str(list(groups.keys())))
            groupName = input("Which group would you like to delete (or enter anything else to not delete)? ")
            if groupName in groups:
                del_group(games, groupName, groups)
            else:
                print("Sorry, that's not one of the groups")
        elif doWhat.lower() == "edit":
            addOrRemove = input("Do you want to add games to a group or remove games from a group?"
                                +" Type 'add' or 'remove': ")
            skip = False
            if addOrRemove.lower() == "add":
                print("The current groups are: " + str(list(groups.keys())))
                groupName = input("What group do you want to add to? ")
                if groupName not in groups:
                    print("Sorry, that's not one of the groups")
                else:
                    for i in range(len(games)):
                        gameToAdd = input("Type the name of a game to add or 'stop' to quit: ")
                        if gameToAdd.lower() == "stop":
                            skip = True
                            break
                        add_game_to_group(games,gameToAdd,groupName, groups)
            elif addOrRemove.lower() == "remove":
                print("The current groups are: " + str(list(groups.keys())))
                groupName = input("What group do you want to remove from? ")
                if groupName not in groups:
                    print("Sorry, that's not one of the groups")
                else:
                    for i in range(len(games)):
                        gameToRemove = input("Type the name of a game to remove or 'stop' to quit: ")
                        if gameToRemove.lower() == "stop":
                            skip = True
                            break
                        del_game_from_group(games,gameToRemove,groupName, groups)
            else:
                print("Sorry, that's not a recognized command")
            if skip:
                continue
        elif doWhat.lower() == "print":
            print("The current groups are: " + str(list(groups.keys())))
            whatGroup = input("What group do you want to print? ")
            if whatGroup not in groups:
                print("Sorry, that's not one of the groups")
            else:
                print_members_of_group(whatGroup, groups)
        else:
            print("Sorry, that's not a recognized command")
            continue


    elif command.lower() == "quit":
        print("Exited SteamManager")
        break


    else:
        print("Sorry, that's not a recognized command")