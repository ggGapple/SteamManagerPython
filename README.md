# SteamManagerPython
A Python-based command-line tool for users to keep track of Steam games with lots of added functionality; similar to Letterboxd, but for video games and fully local on a user's computer (+ with added functionality)

## How to Use
[SteamManager.py](SteamManagerPython/SteamManager.py) is the only file that needs to be run, the rest contain imports for it. Download all the code and run [SteamManager.py](SteamManagerPython/SteamManager.py), which will give a warning about not having [config](SteamManagerPython/config.py) data -- the file will walk through how to set that up, and then the program is fully functional.
The next step would be to obtain game data from Steam (via commands given) and write that to games.json. From there, all commands work and are usable.

## Functionality
The program can:
- Obtain game data (library + playtimes) from Steam via an api key and Steam username
- Obtain and save data to games.json
- Display game data
- Allow the user to rate games, and sort by rating
- Add/remove games to game data
- Edit a game's data
- Add/edit/remove tags from a game
- Add/edit/remove groups for a game
- Recommend games given parameters
