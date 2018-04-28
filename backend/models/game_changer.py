import random
from constants import *

class GameChanger():
    """
        - class representation of a single game changer
        :ivar gameChangerId: the unique identifier of the game changer, check the data dictionary
        :ivar description: a long description of the game changer
        :ivar name: a short description of the game changer
        :ivar weight: a number which determines the probability of the game changer to be selected
        :ivar minWidthIndex, maxWidthIndex: these two variables determine the range which determine whether the game changer has been selected or not depending on the outcome of the die, the minimum index is inclusive while the maximum index is exclusive
        :ivar count: used during testing to see how the number of times the game changer is selected matches its probability
    """

    def __init__(self, description, gameChangerId,name,weight = 1):
        self.gameChangerId = gameChangerId
        self.description = description
        self.name = name
        self.weight = weight
        self.minWidthIndex = -1
        self.maxWidthIndex = -1
        self.count = 0

    def setWidthLimits(self, min):
        """
            - sets the lower and upper limits for this game changer, the range is used to check whether the game changer has been selected or not
            :param min: the lower limit, this comes from the upper limit of the previous game changer, zero for the first game changer to be created
            :type min: int
            :return: None
        """
        self.minWidthIndex = min
        self.maxWidthIndex = min + self.weight

    def getMaxWidthIndex(self):
        """
            - returns the upper limit of this game changer's range
            :return: the upper limit of this game changer's range
            :rtype: int
        """
        return self.maxWidthIndex

    def isSelectedGameChanger(self, selectedIndex):
        """
            - checks whether the selected game changer from the die is withing this game changer's range
            :param selectedIndex: the randomly selected game changer
            :type selectedIndex: int
            :return: True if the randomly selected game changer lies withing this game changer's range, False otherwise
            :rtype: bool
        """
        return selectedIndex >= self.minWidthIndex and selectedIndex < self.maxWidthIndex

    def __repr__(self):
        """ string representation of the gameChanger object """
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
        """
            - sets the lower and upper limits indexes for each game changer depending on its weight
            - the first game changer starts with a lower limit of zero
            - the upper limit of the last game changer determines the width from which the die selection can be calculated
        """
        startMinIndex = 0
        for key, value in self.changers.items():
            value.setWidthLimits(startMinIndex)
            startMinIndex = value.getMaxWidthIndex()
        self.maxWidthLimit = startMinIndex

    def getGameChanger(self,id):
        """
            - given the id of the game changer, the respective game changer object is returned
            :param id: the id of the game changer
            :type id: int
            :return: gameChanger object
            :rtype: gameChanger
        """
        return self.changers[id]

    def rollDie(self):
        """
            - randomly selects a number between zero and the maxWidthLimit and finds the gameChanger in which the selection lies
            :return: the selected gameChanger, None if the gameChanger is not found, technically None should never be returned if the algorithm is correct
            :rtype: gameChanger
        """
        selected = random.randint(0, self.maxWidthLimit - 1)
        for key, value in self.changers.items():
            if value.isSelectedGameChanger(selected):
                return value
        return None
