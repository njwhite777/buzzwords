#!/usr/bin/env python
import datetime
import random
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from .player import Player
from .game_changer import *
from .timer import Timer
from . import Base
from constants import *
from app import turnTimers,Session
import json

class Turn(Base):

    __tablename__ = 'turn'
    id          = Column(Integer,primary_key=True)
    numberOfSkips = Column(Integer)
    startTime = Column(DateTime, default=datetime.datetime.utcnow)
    gameChangerNumber = Column(Integer)
    duration = Column(Integer)
    cardId = Column(Integer, ForeignKey('card.id'), nullable=True)
    turnDuration = Column(Integer)

    gameId = Column(Integer, ForeignKey('game.id'), nullable=False)
    # Don't need to do this. Should already exist cause of backref.
    # game = relationship("Game", foreign_keys=gameId, lazy = False, uselist=False)

    roundId = Column(Integer, ForeignKey('round.id'), nullable=True)
    round = relationship("Round", foreign_keys=roundId, lazy = False, uselist=False)

    teamId = Column(Integer, ForeignKey('team.id'), nullable=True)
    card = relationship("Card", foreign_keys=cardId, lazy = False,post_update=True)

    turnTellerId = Column(Integer, ForeignKey('player.id'), nullable=True)
    teller = relationship('Player', foreign_keys=turnTellerId,post_update=True)

    turnModeratorId = Column(Integer, ForeignKey('player.id'), nullable=True)
    moderator = relationship('Player', foreign_keys=turnModeratorId,post_update=True )


    def __init__(self,game,round,team,turnDuration=30):
        self.numberOfSkips = 0
        self.gameChangerNumber = -1
        self.turnDuration = turnDuration
        self.card = None
        self.game = game
        self.gameId = game.id
        self.round = round
        self.team = team

    @staticmethod
    def getTurnById(turnID,session):
        return session.query(Turn).get(int(turnID))

    def setTeam(self, team):
        self.team = team

    def getTeamsNotOnTurn(self, game):
        teamsNotOnTurn = []
        for theTeam in game.teams:
            if theTeam.id != self.team.id:
                teamsNotOnTurn.append(theTeam)
        return teamsNotOnTurn

    def getRandomTeam(self, teams):
        numberOfTeams = len(teams)
        randomTeamIndex = random.randint(0, numberOfTeams - 1)
        selectedTeam = teams[randomTeamIndex]
        return selectedTeam

    def getRandomPlayer(self, players):
        numberOfPlayers = len(players)
        randomPlayerIndex = random.randint(0, numberOfPlayers - 1)
        return players[randomPlayerIndex]

    def setGameChanger(self):
        gameChangers = GameChangers()
        selectedGameChanger = gameChangers.rollDie()
        self.gameChangerNumber = selectedGameChanger.gameChangerId
        self.updatePlayerRoles()
        return selectedGameChanger

    def getGameChanger(self):
        gameChangers = GameChangers()
        return gameChangers.getGameChanger(self.gameChangerNumber)

    '''
    if the ALL_GUESSERS game changer is selected we have to change all observers to guessers
    '''
    def updatePlayerRoles(self):
        session = Session.object_session(self)
        if self.gameChangerNumber == ALL_GUESSERS:
            observers = self.getObservers()
            for observer in observers:
                observer.role = GUESSER
            session.commit()

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

    def getGuessers(self):
        return self.round.game.getGuessers()

    def getObservers(self):
        return self.round.game.getObservers()

    def getTeller(self):
        return self.teller

    def getModerator(self):
        return self.moderator

    def loadCard(self):
        # game. should work in this context because of the backref to turn from game.
        unusedCards = self.round.game.getUnusedCards()
        if len(unusedCards) == 0:
            return None
        # we might mind to implement a more elegant algorithm which picks a card depending on the stats
        # like number of times gotten right or missed
        card = self.__getRandomUnusedCard(unusedCards)
        self.card = card

        cardData = {
            'card': {
                'buzzword' : card.buzzword,
                'forbiddenwords': json.loads(card.forbiddenWords),
                'phrase' : card.isPhrase,
            },
            'showCard' : True
        }

        self.round.game.addUsedCard(card)
        if self.gameChangerNumber == NO_EXCLUDED_WORDS:
            cardData['forbiddenwords'] = ""
        return cardData

    # def canSkip(self):
    #     if():
    #         return
    #     elif(self.numberOfSkips < 3):
    #     return self.gameChangerNumber == UNLIMITED_SKIPS # number of skips from the game

    def skip(self):
        currentCard = self.card
        currentCard.skippedCount += 1
        self.numberOfSkips += 1
        skipPenaltyAfter = self.round.game.skipPenaltyAfter
        if(self.numberOfSkips > skipPenaltyAfter):
            self.penaliseTeam()

    def awardTeam(self):
        self.card.wonCount += 1
        self.team.score += 1

    def penaliseTeam(self):
        self.card.lostCount += 1
        self.team.score -= 1

    def startTimer(self,callback=None):
        players=self.round.game.getAllPlayers()
        playerEmails = [ player.email for player in players ]
        duration = self.turnDuration
        if( DOUBLE_ROUND_TIME == self.gameChangerNumber ):
            duration*=2
        elif( HALF_ROUND_TIME == self.gameChangerNumber ):
            duration*=.5
        timer = Timer(duration=duration,playerEmails=playerEmails,gameID=self.round.game.id,completeCallback=callback)
        turnTimers[self.id]=timer
        timer.start()

    def getTimer(self):
        return turnTimers[self.id]

    def removeTimer(self):
        del turnTimers[self.id]

    def __repr__(self):
        return "<Turn(id:{})>".format(self.id)
