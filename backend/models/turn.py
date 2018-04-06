#!/usr/bin/env python
import datetime
import random
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from .player import Player
from .game_changer import *
from . import Base
from constants import *

class Turn(Base):

    __tablename__ = 'turn'
    id          = Column(Integer,primary_key=True)
    numberOfSkips = Column(Integer)
    startTime = Column(DateTime, default=datetime.datetime.utcnow)
    gameChangerNumber = Column(Integer)
    roundId = Column(Integer, ForeignKey('round.id'), nullable=False)
    cardId = Column(Integer, ForeignKey('card.id'), nullable=True)
    card = relationship("Card", foreign_keys=cardId, lazy = False)
    teamId = Column(Integer, ForeignKey('team.id'), nullable=True)
    turnTellerId = Column(Integer, ForeignKey('player.id'), nullable=True)
    turnModeratorId = Column(Integer, ForeignKey('player.id'), nullable=True)
    teller = relationship('Player', foreign_keys=turnTellerId )
    moderator = relationship('Player', foreign_keys=turnModeratorId )

    def __init__(self, team):
        self.numberOfSkips = 0
        self.gameChangerNumber = 1 # don't change, __setGuessers depends on this as of now
        self.card = None
        self.team = team

    def setTeam(self, team):
        self.team = team

    def getTeamsNotOnTurn(self, game):
        teamsNotOnTurn = []
        for theTeam in game.teams:
            if self.team.id != theTeam.id:
                teamsNotOnTurn.append(theTeam)
        return teamsNotOnTurn

    def getRandomTeam(self, teams):
        numberOfTeams = len(teams)
        randomTeamIndex = random.randint(0, numberOfTeams - 1)
        selectedTeam = teams[randomTeamIndex]
        return selectedTeam

    def getRandomPlayer(self, players):
        numberOfPlayers = len(players)
        print("players:>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + str(numberOfPlayers))
        randomPlayerIndex = random.randint(0, numberOfPlayers - 1)
        return players[randomPlayerIndex]

    def setGameChanger(self):
        gameChangers = GameChangers()
        selectedGameChanger = gameChangers.rollDie()
        self.gameChangerNumber = selectedGameChanger.gameChangerId

    '''
    if the ALL_GUESSERS game changer is selected we have to change all observers to guessers
    '''
    def updatePlayerRoles(self, game):
        if self.gameChangerNumber == ALL_GUESSERS:
            observers = self.getObservers(game)
            for observer in observers:
                observer.role = GUESSER

    def __getRandomUnusedCard(self, cards):
        numberOfCards = len(cards)
        randomCardIndex = random.randint(0, numberOfCards - 1)
        return cards[randomCardIndex]

    def setPlayerRoles(self, game):
        self.__setObservers(game)
        self.__setGuessers(game)
        self.__setTeller()
        self.__setModerator(game)

    def __setModerator(self, game):
        teamsNotOnTurn = self.getTeamsNotOnTurn(game)
        randomTeam = self.getRandomTeam(teamsNotOnTurn)
        moderator = self.getRandomPlayer(randomTeam.players)
        moderator.role = 2
        self.moderator = moderator
        return moderator

    def __setTeller(self):
        teller = self.getRandomPlayer(self.team.players)
        teller.role = 1
        self.teller = teller
        return teller

    def __setObservers(self, game):
        teamsNotOnTurn = self.getTeamsNotOnTurn(game)
        for team in teamsNotOnTurn:
            players = team.players
            for player in players:
                player.role = OBSERVER

    def __setGuessers(self, game):
        if self.gameChangerNumber == ALL_GUESSERS:
            guessers = game.getAllPlayers()
        else:
            guessers = self.team.players
        for guesser in guessers:
            guesser.role = GUESSER

    def getGuessers(self, game):
        return game.getGuessers()

    def getObservers(self, game):
        return game.getObservers()

    def getTeller(self):
        return self.teller

    def getModerator(self):
        return self.moderator

    def loadCard(self, session, game):
        unusedCards = game.getUnusedCards(session)
        if len(unusedCards) == 0:
            return None
        # we might mind to implement a more elegant algorithm which picks a card depending on the stats
        # like number of times gotten right or missed
        card = self.__getRandomUnusedCard(unusedCards)
        self.card = card
        game.addUsedCard(card)
        # takes care of the no forbidden words game changer
        if self.gameChangerNumber == NO_EXCLUDED_WORDS:
            card.removeForbiddenWords()
        return card

    def canSkip(self):
        pass


    def __repr__(self):
        return "<GameRound()>".format()
