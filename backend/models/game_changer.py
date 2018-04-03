import random

class GameChanger():

    def __init__(self, description, gameChangerId, weight = 1):
        self.gameChangerId = gameChangerId
        self.description = description
        self.weight = weight
        self.minWidthIndex = -1
        self.maxWidthIndex = -1

    def setWidthLimits(self, min):
        self.minWidthIndex = min
        self.maxWidthIndex = min + self.weight

    def getMaxWidthIndex(self):
        return self.maxWidthIndex

    def isSelectedGameChanger(self, selectedIndex):
        return selectedIndex >= self.minWidthIndex and selectedIndex < self.maxWidthIndex


class  GameChangers():

    def __init__(self):
        self.maxWidthLimit = -1
        self.changers = dict()
        self.changers[0] = GameChanger("double round time", 0, 1)
        self.changers[1] = GameChanger("half round time", 1, 4)
        self.changers[2] = GameChanger("unlimited skips: The teller can skip unlimited number of cards in one round", 2, 4)
        self.changers[3] = GameChanger("No excluded words: Only the main word will be visible in the card. The teller can explain without worrying about the excluded words", 3, 8)
        self.changers[4] = GameChanger("Statue teller: The teller will explain the word while standing like a statue only by talking. No part of his/her body will move except mouth.", 4, 16)
        self.changers[5] = GameChanger("One-person teller: The teller will explain to only one of the guessers. The remaining of the guessers will stay silent during the round.", 5, 16)
        self.changers[6] = GameChanger("Round-killer: Current team missed its round completely. It is next team’s turn now.", 6, 10)
        self.changers[7] = GameChanger("All guessers: Any member of the other team can also guess along with guessers. Whoever can guess the word will be rewarded with one point to his/her team.", 7, 10)

    def setGameChangerWidthLimits(self):
        startMinIndex = 0
        for key, value in self.changers.items():
            value.setWidthLimits(startMinIndex)
            startMinIndex = value.getMaxWidthIndex()
        #print("max===================================================: " + str(self.maxWidthLimit))
        self.maxWidthLimit = startMinIndex

    def rollDie(self):
        self.setGameChangerWidthLimits()
        selected = random.randint(0, self.maxWidthLimit - 1)
        print("max===================================================: " + str(self.maxWidthLimit))
        print("selected===================================================: " + str(selected))
        for key, value in self.changers.items():
            if value.isSelectedGameChanger(selected):
                return value
        return None
