# Game Status Constants
GAME_CREATED = 1 # the game has been created but is not ready / valid to start
GAME_READY = 2 # the game can be started
GAME_PLAYING = 3 # the game has been started and is in playing mode
GAME_PAUSED = 4 # the game has been paused
GAME_COMPLETE = 5 # the game is over

# Player roles constants
TELLER = 1
MODERATOR = 2
GUESSER = 3
OBSERVER = 4 # if to be considered, player who is neither the moderator nor the teller and his team is not on deck

# Game Changers constants
DOUBLE_ROUND_TIME = 0
HALF_ROUND_TIME = 1
UNLIMITED_SKIPS = 2
NO_EXCLUDED_WORDS = 3
STATUE_TELLER = 4
ONE_PERSON_TELLER = 5
ROUND_KILLER = 6
ALL_GUESSERS = 7
