#!/usr/bin/env python
import time
import random
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from .player import Player
from . import Base

class Turn(Base):

    __tablename__ = 'turn'
    id          = Column(Integer,primary_key=True)
    number         = Column(Integer)
    numberOfSkips = Column(Integer)
    startTime = Column(DateTime)
    gameChangerNumber = Column(Integer)
    roundId = Column(Integer, ForeignKey('round.id'), nullable=False)
    cardId = Column(Integer, ForeignKey('card.id'), nullable=True)
    card = relationship("Card", foreign_keys=cardId, lazy = False)
    teamId = Column(Integer, ForeignKey('team.id'), nullable=True)
    turnTellerId = Column(Integer, ForeignKey('player.id'), nullable=True)
    turnModeratorId = Column(Integer, ForeignKey('player.id'), nullable=True)
    teller = relationship('Player', foreign_keys=turnTellerId )
    moderator = relationship('Player', foreign_keys=turnModeratorId )

    def __init__(self, number):
        self.number = number
        self.numberOfSkips = 0
        self.startTime = time.time()
        self.gameChangerNumber = 3
        self.card = None

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
        selectedTeam = teamsNotOnTurn[randomTeamIndex]
        return selectedTeam

    def getRandomPlayer(self, players):
        players = selected_team.players
        numberOfPlayers = len(players)
        randomPlayerIndex = random.randint(0, numberOfPlayers - 1)
        return players[randomPlayerIndex]

    def getRandomUnusedCard(self, cards):
        numberOfCards = len(cards)
        randomCardIndex = random.randint(0, numberOfCards - 1)
        return cards[randomCardIndex]

    def setModerator(self, game):
        teamsNotOnTurn = self.getTeamsNotOnTurn(game)
        randomTeam = self.getRandomTeam(teamsNotOnTurn)
        moderator = self.getRandomPlayer(randomTeam.players)
        moderator.role = 2
        self.moderator = moderator
        return moderator

    def setTeller(self):
        teller = self.getRandomPlayer(self.team.players)
        teller.role = 1
        self.teller = teller
        return teller

    def loadCard(self, game):
        unusedCards = game.getUnusedCards()
        if len(unusedCards) == 0:
            return None
        # we might mind to implement a more elegant algorithm which picks a card depending on the stats
        # like number of times gotten right or missed
        card = self.getRandom_unusedCard()
        self.card = card # sets a new card to the turn
        game.addUsedCard(card)
        return card

    def canSkip(self):
        pass


    def __repr__(self):
        return "<GameRound()>".format()
