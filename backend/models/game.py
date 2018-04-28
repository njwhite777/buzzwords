#!/usr/bin/env python
import datetime
from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, and_
from sqlalchemy.orm import sessionmaker, relationship
from .card import Card
from .round import Round
from .turn import Turn
from . import Base
from constants import *
from .validator import *
import globalVars

# association table with the gameID and cardID to keep track of the cards used in a particular game
usedCards = Table('used_cards',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('game.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('card.id'), primary_key=True)
)

class Game(Base):
    """
        - the class representaion of the game
        :ivar id: the primary key of the table
        :ivar name: the name of the game, must be between 2 and 255 characters inclusive
        :ivar gameState: the game can be in one of the 5 states:
            GAME_CREATED = 1 # the game has been created but is not ready / valid to start
            GAME_READY = 2 # the game can be started
            GAME_PLAYING = 3 # the game has been started and is in playing mode
            GAME_PAUSED = 4 # the game has been paused
            GAME_COMPLETE = 5 # the game is over
        :ivar turnDuration: the default duration of the turn in seconds, provide by the game creator
        :ivar withGameChangers: the value which tells whether game is to be played with or without game changers,currently not used, will be added in the next version
        :ivar pointsToWin: the number of points if reached by one or more teams the game is over after all teams have played equal number of turns, provided by the game creator
        :ivar maxPlayersPerTeam: the maximum number of accpted players in team, provided by the game creator
        :ivar numberOfTeams: number of teams in the game, privided by the game creator
        :ivar skipPenaltyAfter: the number of free skips provided in each turn, has no impact if UNLIMITED_SKIPS game changer is selected
        :ivar minRequiredPlayers: the minimum number of players allowed in the team, the default is two(2)
        :ivar createdTimeStamp: date and time the game has been created
        :ivar initiatorID: the foreign key from the player table to keep track of the game creator
        :ivar initiator: the player who iniated the game
        :ivar teams: the list of teams in the game
        :ivar rounds: the list of rounds in the game
        :ivar usedCards: the list of cards which have already been used in the game
    """

    __tablename__ = 'game'
    id   = Column(Integer, primary_key=True)
    name = Column(String(256))
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
    teams = relationship("Team", backref = "game", lazy = False, order_by = "Team.id")
    rounds = relationship("Round", backref = "game", lazy = False)
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
        self.usedCards = []
        self.players = []
        self.rounds = []
        self.teams = []

    @staticmethod
    def numberOfRows(session):
        """
            - returns number of all games created in the system
            :return: the number of all games created in the system
            :rtype: int
        """
        return session.query(Game).count()

    @staticmethod
    def isValidGame(session, data):
        """
            - validates the game details received from the client, also checks that the game name does not exist from the list of games not yet playable
            :param data: game info received from the client
            :type data: dictionary
            :param session: database session
            :type session: sqlalchemy.Session
            :return: a dictionary with valid = True if all the data is valid, if part of the data is invalid a dictionary with valid = False and message = "error message" is returned
            :rtype: dictionary
        """
        feedback = Validator.isValidGame(data)
        if not feedback['valid']:
            return feedback
        if Game.gameNameExists(session, data['name']):
            return {'valid' : False, 'message' : 'the game name exists'}
        return feedback

    @staticmethod
    def gameNameExists(session, name):
        """
            - checks if the provided game name exists in the list of games which are not yet unplayable
            - the name can only be reused if the game with a name collision has already started (not in the list of the games to be joined)
            :param name: the name of the new game to be created
            :type name: string
            :param session: database session
            :type session: sqlalchemy.Session
            :return: True if the name exists, False otherwise
            :rtype: bool
        """
        game = session.query(Game).filter(and_(Game.name==name, Game.gameState < GAME_PLAYING)).first()
        return game != None

    @staticmethod
    def getGameById(game_id,session):
        """
            - returns the game object with the given game_id
            :param session: database session
            :type session: sqlalchemy.Session
            :param game_id: primary key of the game table
            :type game_id: int
            :return: the game object if the game_id exists, None otherwise
            :rtype: models.Game
        """
        return session.query(Game).get(int(game_id))

    @staticmethod
    def getAllGames(session):
        """
            - returns the list of all games in the system
            :param session: the database session
            :type session: sqlalchemy.Session
            :return: the list of all games in the system
            :rtype: list<models.Game>
        """
        return session.query(Game).all()

    def setStatePaused(self):
        """
            - the state of the game is saved including the timer, resuming restarts the game
            - done by the moderator
        """
        self.gameState=GAME_PAUSED

    def setStateComplete(self):
        """
            - set when the game is over
            - done by the system
        """
        self.gameState=GAME_COMPLETE

    def setStateStart(self):
        """
            - the game is ready to start
            - done when the first turn in the game is started
        """
        self.gameState=GAME_PLAYING

    def setStateReady(self):
        """
            - set when the game is in a valid condition to be started but not yet started
            - done by the system
        """
        self.gameState=GAME_READY

    def addUsedCard(self, card):
        """
            - adds the selected card to the list of used cards so it cannot be used again in the same game
            :param card: the selected card
            :type card: models.Card
        """
        self.usedCards.append(card)

    def addTeam(self,team):
        """
            - add the team in the list of teams participating in this game
            :param team: the new team to be added
            :type team: models.Team
        """
        self.teams.append(team)

    def addRound(self, round):
        """
            - adds a new round in the list of rounds played in the game
            - a new round is created every time the first team starts a new turn
            :param round: the new round to be added to the game
            :type round: models.Round
        """
        self.rounds.append(round)

    def getUsedCards(self):
        """
            - returns the list of all used cards in the game
            :return: the list of used cards
            :rtype: list<models.Card>
        """
        return self.used_cards

    def getAllPlayers(self):
        """
            - returns the list of all players participating in the game
            :return: the list of all players in the game
            :rtype: list<models.Player>
        """
        players = list()
        for team in self.teams:
            players += team.players
        return players

    def getObservers(self):
        """
            - returns the list of all observers in the current turn
            :return: the list of all observers in the current turn
            :rtype: list<models.Player>
        """
        observers = list()
        for player in self.getAllPlayers():
            if player.isObserver():
                observers.append(player)
        return observers

    def getGuessers(self):
        """
            - returns the list of all guessers in the current turn
            :return: the list of all guessers in the current turn
            :rtype: list<models.Player>
        """
        guessers = list()
        for player in self.getAllPlayers():
            if player.isGuesser():
                guessers.append(player)
        return guessers

    def getUsedCardsIds(self):
        """
            - generates and returns a list of used card ids
            - used in generating the query for finding the unused cards
            :return: the list of used card ids
            :rtype: list<int>
        """
        usedCardIds = []
        for card in self.usedCards:
            usedCardIds.append(card.id)
        return usedCardIds

    def getUnusedCards(self):
        """
            - generates the list of unused cards in the game
            :return: the list of all unused cards in the game
            :rtype: list<models.Card>
        """
        session=globalVars.Session()
        query = session.query(Card).filter(~(Card.id.in_(self.getUsedCardsIds())))
        all = query.all()
        session.close()
        return all

    def readyToStart(self):
        """
            - checks if the minimum condition for the game to start are met
            :return: True if the game can start, False otherwise
            :rtype: bool
        """
        for team in self.teams:
            if not(team.validTeam()):
                return False
        return True

    def isGameOver(self):
        """
            - checks if the game is over,
            - the game is over when one of the team has reached the points to win and all teams have played equal number of rounds
            :return: True if the game is over, False otherwise
            :rtype: bool
        """
        if not(self.hasAtLeastOneRound()):
            return False
        elif not(self.teamsHaveEqualTurns()):
            return False
        return self.teamHasReachedThreshold()

    def hasAtLeastOneRound(self):
        """
            - checks if the game has had at least one round
            :return: True if the game has at least a single round, False otherwise
            :rtype: bool
        """
        return len(self.rounds) > 0

    def teamsHaveEqualTurns(self):
        """
            - checks if all teams have played equal number of turns
            - since the teams play in the same order we need not compare each team with every other team
            :return: True if all teams have played equal number of turns, False otherwise
            :rtype: bool
        """
        turns = self.teams[0].numberOfTurns()
        for team in self.teams:
            if team.numberOfTurns() != turns:
                return False
        return True

    def getCurrentRound(self):
        """
            - finds the latest round in the game
            - if no round yet in the game, a new round is created
            :return: the latest added round in the game
            :rtype: models.Round
        """
        session = globalVars.Session.object_session(self)
        if not self.rounds:
            newRound = Round(number=0,game=self)
            self.rounds.append(newRound)
            session.commit()
        return self.rounds[len(self.rounds) - 1]

    def getRoundNextTeam(self, currentTeam):
        """
            - uses the currentTeam on deck to find the team to play the next turn
            :return: the team to play the next turn
            :rtype: models.Team
        """
        index = 0
        for team in self.teams:
            if team.id == currentTeam.id:
                nextIndex = (index + 1) % len(self.teams)
                return self.teams[nextIndex]
            index += 1
        return None

    def createTurn(self):
        """
            - creates a new turn  and adds it to the current round
            - if all teams have played equal number of turns, a new round is created
            :return: new turn created
            :rtype: models.Turn
        """
        session = globalVars.Session.object_session(self)
        currentRound = self.getCurrentRound()
        if self.isRoundOver(currentRound):
            nextRoundNumber = currentRound.number + 1
            newRound = Round(number=nextRoundNumber,game=self)
            self.rounds.append(newRound)
            currentRound = newRound
            session.add(currentRound)
            session.commit()
        lastTurn = currentRound.getCurrentTurn()
        if lastTurn:
            lastTeam = lastTurn.team
            nextTeam = self.getRoundNextTeam(lastTeam)
        else:
            nextTeam = self.teams[0]
        turn = Turn(team=nextTeam,round=currentRound,game=self,turnDuration=self.turnDuration)
        session.add(turn)
        session.commit()
        turn.setPlayerRoles()
        currentRound.addTurn(turn)
        session.commit()
        return turn

    def isRoundOver(self, currentRound):
        """
            - checks if the round is over, i.e all teams have played equla number of rounds
            :return: True if the round is over, False otherwise
            :rtype: bool
        """
        return len(currentRound.turns) == len(self.teams)

    def teamHasReachedThreshold(self):
        """
            - checks if any of the teams has reached the minimum number of points to win the game
            :return: True if any of team has reached the minimum number of points to win the game, False otherwise
            :rtype: bool
        """
        for team in self.teams:
            print(team.name, team.score, self.pointsToWin)
            if team.score >= self.pointsToWin:
                print('we have a winner')
                return True
        return False

    def __repr__(self):
        """
            - returns the string representation of the game object
        """
        return "<Game(id='{}', name='{}', pointsToWin='{}')>".format(
            self.id,self.name,self.pointsToWin)
