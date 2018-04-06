#!/usr/bin/env python
import datetime
from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from .card import Card
from . import Base
from constants import *

usedCards = Table('used_cards',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('game.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('card.id'), primary_key=True)
)

class Game(Base):

    __tablename__ = 'game'
    id   = Column(Integer, primary_key=True)
    name = Column(String)
    gameState = Column(Integer)
    turnDuration = Column(Integer)
    withGameChangers = Column(Integer)
    pointsToWin = Column(Integer)
    maxPlayersPerTeam = Column(Integer)
    numberOfTeams = Column(Integer)
    skipPenaltyAfter = Column(Integer)
    minRequiredPlayers=Column(Integer)
    createdTimeStamp = Column(DateTime, default=datetime.datetime.utcnow)
    initiatorID = Column(Integer, ForeignKey('player.id'), nullable=True)

    initiator = relationship("Player", foreign_keys=initiatorID, lazy = False, uselist=False)
    teams = relationship("Team", backref = "game", lazy = False)
    rounds = relationship("Round",backref = "game", lazy = False)
    usedCards = relationship("Card",secondary=usedCards,lazy = False)

    def __init__(self,initiator,name=None,turnDuration=30,numberOfTeams=2,maxPlayersPerTeam=5,pointsToWin=30,skipPenaltyAfter=3,withGameChangers=1,minRequiredPlayers=2):
        self.name = name
        self.gameState    = GAME_CREATED
        self.turnDuration = turnDuration
        self.withGameChangers = withGameChangers
        self.pointsToWin  = pointsToWin
        self.maxPlayersPerTeam = maxPlayersPerTeam
        self.numberOfTeams = numberOfTeams
        self.minRequiredPlayers = minRequiredPlayers
        self.skipPenaltyAfter = skipPenaltyAfter
        self.initiator = initiator
        self.used_cards = []
        self.players = []
        self.rounds = []
        self.teams = []

    @staticmethod
    def numberOfRows(session):
        return session.query(Game).count()

    @staticmethod
    def getGameById(session, game_id):
        return session.query(Game).get(int(game_id))

    def setStatePaused(self):
        self.gameState=GAME_PAUSED

    def setStateComplete(self):
        self.gameState=GAME_COMPLETE

    def setStateStart(self):
        self.gameState=GAME_PLAYING

    def setStateReady(self):
        self.gameState=GAME_READY

    @staticmethod
    def getAllGames(session):
        return session.query(Game).all()

    def addUsedCard(self, card):
        self.used_cards.append(card)

    def addTeam(self,team):
        self.teams.append(team)

    def addRound(self, round):
        self.rounds.append(round)

    def getUsedCards(self):
        return self.used_cards

    def getAllPlayers(self):
        players = list()
        for team in teams:
            for player in team.players:
                players.append(player)
        return players

    def getObservers(self):
        observers = list()
        for player in self.getAllPlayers():
            if player.isObserver():
                observers.append(player)
        return observers

    def getGuessers(self):
        guessers = list()
        for player in self.getAllPlayers():
            if player.isGuesser():
                guessers.append(player)
        return guessers

    def getUsedCardsIds(self):
        usedCardIds = []
        for card in self.usedCardIds:
            usedCardIds.append(card.id)
        return usedCardIds

    def getUnusedCards(self, session):
        query = session.query(Card).filter(~(Card.id.in_(self.get_used_cards_ids())))
        return query.all()

    def readyToStart(self):
        for team in self.teams:
            if not(team.validTeam()):
                return False
        return True

    def isGameInValidState(self):
        if self.rounds == 0:
            return False
        for team in self.teams:
            if not(team.validTeam()):
                return False
        return True

    def isGameOver(self):
        if not self.hasAtLeastOneRound():
            return False
        elif self.teamsHaveEqualTurns():
            return False

    def hasAtLeastOneRound(self):
        return self.rounds > 0

    def teamsHaveEqualTurns(self):
        turns = self.teams.numberOfTurns()
        for team in self.teams:
            if team.numberOfTurns() != turns:
                return False
        return True

    def teamHasReachedThreshold():
        pass

    def __repr__(self):
        return "<Game(id='{}', name='{}', pointsToWin='{}')>".format(
            self.id,self.name,self.pointsToWin)
