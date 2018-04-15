import random
from constants import *

class GameChanger():

    def __init__(self, description, gameChangerId,name,weight = 1):
        self.gameChangerId = gameChangerId
        self.description = description
        self.name = name
        self.weight = weight
        self.minWidthIndex = -1
        self.maxWidthIndex = -1
        self.count = 0

    def setWidthLimits(self, min):
        self.minWidthIndex = min
        self.maxWidthIndex = min + self.weight

    def getMaxWidthIndex(self):
        return self.maxWidthIndex

    def isSelectedGameChanger(self, selectedIndex):
        return selectedIndex >= self.minWidthIndex and selectedIndex < self.maxWidthIndex

    def __repr__(self):
        return "<GameChanger(id:{},weight:{},description:{})>".format(self.gameChangerId,self.weight,self.description)

class  GameChangers():

    def __init__(self,withNorm=False):
        self.maxWidthLimit = -1
        self.changers = dict()
        changersList = list()
        if(withNorm):
            changersList=changersList=[ GameChanger("Double Turn Time: Turn duration will be doubled!", DOUBLE_ROUND_TIME,'2X Turn', 2),GameChanger("Half Turn Time: Turn duration will cut in half!.", HALF_ROUND_TIME,'.5X Turn', 7),
            GameChanger("Infinite Skips: The teller can skip unlimited number of cards in one round", UNLIMITED_SKIPS,'∞ Skips', 7),GameChanger("No Forbidden Words: Only the buzzword will be visible in the card.", NO_EXCLUDED_WORDS,'No Forbidden Words', 14),
            GameChanger("Statue Teller: The teller will explain the word while standing like a statue only by talking. No part of his/her body will move except mouth.", STATUE_TELLER,'Statue Teller', 15),
            GameChanger("One Guesser: The teller will explain to only one of the guessers. You may choose which guesser will represent your team!", ONE_GUESSER,'One Guesser', 15),
            GameChanger("Turn Killer: Your turn is lost! Sorry, but it's the next team’s turn now.", ROUND_KILLER,'Round Killer', 14),
            GameChanger("All Guessers: All members of the other teams may guess along your team's guessers. Whoever can guess the word will be rewarded with one point to his/her team.", ALL_GUESSERS,'All Guessers', 14),
            GameChanger("Normal Turn: No modifiers applied this turn!", NORMAL_TURN,'Normal Turn', 12)]
        else:
            changersList=[ GameChanger("Double Turn Time: Turn duration will be doubled!", DOUBLE_ROUND_TIME,'2X Turn', 2),GameChanger("Half Turn Time: Turn duration will cut in half!.", HALF_ROUND_TIME,'.5 Turn', 7),
            GameChanger("Infinite Skips: The teller can skip unlimited number of cards in one round", UNLIMITED_SKIPS,'∞ Skips', 7),GameChanger("No Forbidden Words: Only the buzzword will be visible in the card.", NO_EXCLUDED_WORDS,'No Forbidden Words', 14),
            GameChanger("Statue Teller: The teller will explain the word while standing like a statue only by talking. No part of his/her body will move except mouth.", STATUE_TELLER,'Statue Teller', 21),
            GameChanger("One Guesser: The teller will explain to only one of the guessers. You may choose which guesser will represent your team!", ONE_GUESSER,'One Guesser', 21),
            GameChanger("Turn Killer: Your turn is lost! Sorry, but it's the next team’s turn now.", ROUND_KILLER,'Round Killer', 14),
            GameChanger("All Guessers: All members of the other teams may guess along your team's guessers. Whoever can guess the word will be rewarded with one point to his/her team.", ALL_GUESSERS,'All Guessers', 14)]

        for idx,item in enumerate(changersList):
            self.changers[idx] = item

        self.setGameChangerWidthLimits()

    def setGameChangerWidthLimits(self):
        startMinIndex = 0
        for key, value in self.changers.items():
            value.setWidthLimits(startMinIndex)
            startMinIndex = value.getMaxWidthIndex()
        self.maxWidthLimit = startMinIndex

    def getGameChanger(self,id):
        return self.changers[id]

    def rollDie(self):
        selected = random.randint(0, self.maxWidthLimit - 1)
        for key, value in self.changers.items():
            if value.isSelectedGameChanger(selected):
                return value
        return None
