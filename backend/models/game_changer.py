class GameChanger():

    def __init__(self, description, game_changer_id, weight = 1):
        self.game_changer_id = game_changer_id
        self.description = description
        self.weight = weight
        self.min_width_index = -1
        self.max_width_index = -1

    def setWidthLimits(self, min):
        self.min_width_index = min
        self.max_width_index = min + self.weight

    def isSelectedGameChanger(self, selectedIndex):
        return self.min_width_index >= selectedIndex and self.max_width_index < selectedIndex


class  GameChangers():

    def __init__(self):
        self.changers = dict()
        self.changers[0] = GameChanger("double round time", 0)
        self.changers[1] = GameChanger("half round time", 1)
        self.changers[2] = GameChanger("unlimited skips: The teller can skip unlimited number of cards in one round", 2)
        self.changers[3] = GameChanger("No excluded words: Only the main word will be visible in the card. The teller can explain without worrying about the excluded words", 3)
        self.changers[4] = GameChanger("Statue teller: The teller will explain the word while standing like a statue only by talking. No part of his/her body will move except mouth.", 4)
        self.changers[5] = GameChanger("One-person teller: The teller will explain to only one of the guessers. The remaining of the guessers will stay silent during the round.", 5)
        self.changers[6] = GameChanger("Round-killer: Current team missed its round completely. It is next team’s turn now.", 6)
        self.changers[7] = GameChanger("All guessers: Any member of the other team can also guess along with guessers. Whoever can guess the word will be rewarded with one point to his/her team.", 7)

    def rollDie(self):
        pass
