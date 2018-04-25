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
import json
from .team import Team as TeamModel
import globalVars


class Turn(Base):
    """
        - the object representation of a turn
        :ivar id: the primary key of the table
        :ivar numberOfSkips: the number of times the team can skip in a turn without being penalized, refreshed after every turn
        :ivar startTime: the time the turn started
        :ivar gameChangerNumber: the id of the selected game changer number
        :ivar duration: duration of the turn, can vary depending on the game changer
        :ivar cardId: a foreign key from the card table to keep track of the card being played, updated every time there is infraction, a card is skipped or a point is awarded for getting the correct guess
        :ivar turnDuration: duplicate
        :ivar gameId: a foreign key from the game table to keep track of the game in which the turn belongs
        :ivar roundId: a foreign key from the round table to keep track of the round in which the turn belongs
        :ivar teamId: a foreign key from the team table to keep track of the team playing the turn
        :ivar card: the card being played
        :ivar turnTellerId: the foreign key to the player table containing the id the player with a "teller role"
        :ivar turnModeratorId: the foreign key to the player table containing the id the player with a "moderator role"
        :ivar teller: the player whose role is the teller, changed in each turn
        :ivar moderator: the player whose role is the moderator, changed in each turn
    """

    __tablename__ = 'turn'
    id          = Column(Integer,primary_key=True)
    numberOfSkips = Column(Integer)
    startTime = Column(DateTime, default=datetime.datetime.utcnow)
    gameChangerNumber = Column(Integer)
    duration = Column(Integer)
    cardId = Column(Integer, ForeignKey('card.id'), nullable=True)
    turnDuration = Column(Integer)

    gameId = Column(Integer, ForeignKey('game.id'), nullable=False)
    roundId = Column(Integer, ForeignKey('round.id'), nullable=True)
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
        """
            - creates and returns the Turn object with the given primary key
            :param turnID: the primary key of the turn table
            :type turnID: int
            :param session: the database session
            :type session: sqlalchemy.Session
            :return: Turn object if the primary key exists, None otherwsie
            :rtype: Turn
        """
        return session.query(Turn).get(int(turnID))

    def setTeam(self, team):
        """
            - sets the team playing this turn
            :param team: the Team playing this turn
            :type team: Team
        """
        self.team = team

    def getTeamsNotOnTurn(self):
        """
            - returns the list of all teams which are not on deck
            :param game: the game object in which the turn belongs
            :type game: models.Game
            :return: the list of all teams not on deck, empty list if none exists
            :rtype: list
        """
        teamsNotOnTurn = []
        game = self.round.game
        for theTeam in game.teams:
            if theTeam.id != self.team.id:
                teamsNotOnTurn.append(theTeam)
        return teamsNotOnTurn

    def getRandomTeam(self, teams):
        """
            - finds a random team from the list of given teams, throws exception if the list is empty
            :param teams: the list of given teams
            :type teams: list<models.Team>
            :return: the selected team
            :rtype: models.Team
        """
        numberOfTeams = len(teams)
        randomTeamIndex = random.randint(0, numberOfTeams - 1)
        selectedTeam = teams[randomTeamIndex]
        return selectedTeam

    def getRandomPlayer(self, players):
        """
            - returns a random player from the list of given players, throws exception if the list is empty
            :param players: the list of given players
            :type players: list<models.Player>
            :return: the selected player
            :rtype: models.Player
        """
        numberOfPlayers = len(players)
        randomPlayerIndex = random.randint(0, numberOfPlayers - 1)
        return players[randomPlayerIndex]

    def setGameChanger(self):
        """
            - selects and sets the game changer id to the turn
            :return: the selected game changer object
            :rtype: models.GameChanger
        """
        gameChangers = GameChangers(withNorm=True)
        selectedGameChanger = gameChangers.rollDie()
        self.gameChangerNumber = selectedGameChanger.gameChangerId
        self.updatePlayerRoles()
        return selectedGameChanger

    def getGameChanger(self):
        """
            - returns the selected game changer object
            :return: the selected game changer
            :rtype: models.GameChanger
        """
        gameChangers = GameChangers(withNorm=True)
        return gameChangers.getGameChanger(self.gameChangerNumber)

    def updatePlayerRoles(self):
        """
            - updates player roles, this happends when the ALL_GUESSERS game changer has been selected in which case all observers have to be updated to guessers
        """
        session = globalVars.Session.object_session(self)
        if self.gameChangerNumber == ALL_GUESSERS:
            observers = self.getObservers()
            for observer in observers:
                observer.role = GUESSER
            session.commit()

    def __getRandomUnusedCard(self, cards):
        """
            - finds and returns a random card from the list of given cards
            :param cards: a list of cards
            :type cards: list<models.Card>
            :return: the selected card
            :rtype: models.Card
        """
        numberOfCards = len(cards)
        randomCardIndex = random.randint(0, numberOfCards - 1)
        return cards[randomCardIndex]

    def setPlayerRoles(self):
        """
            - sets the roles of all players before the turn starts
            - the order matters here,
                __setObservers will update the moderator's role if called after __setModerator
                __setGuessers will update the teller's role if called after __setTeller
        """
        self.__setObservers()
        self.__setGuessers()
        self.__setTeller()
        self.__setModerator()

    def __setModerator(self):
        """
            - randomly selects a player from one of the teams not on deck to be the moderator
            - should be called after __setModerator to avoid updating the moderator's role
        """
        teamsNotOnTurn = self.getTeamsNotOnTurn()
        randomTeam = self.getRandomTeam(teamsNotOnTurn)
        moderator = self.getRandomPlayer(randomTeam.players)
        moderator.role = 2
        self.moderator = moderator
        return moderator

    def __setTeller(self):
        """
            - finds the player from the team on deck to be teller, the teller role cycles through all players in a team
            - should be called after the __setGuessers method to avoid updating the teller's role
            :return: the selected player
            :rtype: models.Player
        """
        tellerID = self.round.number % len(self.team.players)
        teller = self.team.players[tellerID]
        teller.role = 1
        self.teller = teller
        return teller

    def __setObservers(self):
        """
            - sets all players whose team is not on deck to be observers,
            - one player is chosen in the __setModerator method to be the moderator leaving the other player roles intact
        """
        teamsNotOnTurn = self.getTeamsNotOnTurn()
        for team in teamsNotOnTurn:
            players = team.players
            for player in players:
                player.role = OBSERVER

    def __setGuessers(self):
        """
            - sets the players whose team is on deck to be the guessers
            - the __setTeller method is called after to update one player from the list to be the teller
        """
        game = self.round.game
        if self.gameChangerNumber == ALL_GUESSERS:
            guessers = game.getAllPlayers()
        else:
            guessers = self.team.players
        for guesser in guessers:
            guesser.role = GUESSER

    def getAllTeamScores(self):
        """
            - returns the score of each team in the game
            :return: the dictionary containing the score of each team in the game
            :rtype: dictionary
        """
        teamScoreData = dict()
        teams = self.round.game.teams
        for team in teams:
            tDict = {
                'teamID': team.id,
                'id' : team.id,
                'name': team.name,
                'score' : team.score,
                'out_of': self.round.game.pointsToWin
            }
            teamScoreData[team.id] = tDict
        return teamScoreData

    def getGuessers(self):
        """
            - returns the list of players who are guessers in this turn
            :return: list of guessers in the turn
            :rtype: list<models.Player>
        """
        return self.round.game.getGuessers()

    def getObservers(self):
        """
            - returns the list of players who are observers in this turn
            :return: list of observers in the turn
            :rtype: list<models.Player>
        """
        return self.round.game.getObservers()

    def getTeller(self):
        """
            - returns the teller in the turn
            :return: the teller in the turn
            :rtype: models.Player
        """
        return self.teller

    def getModerator(self):
        """
            - returns the moderator in the turn
            :return: the moderator in the turn
            :rtype: models.Player
        """
        return self.moderator

    def loadCard(self):
        """
            - randomly selects a card from the list of unused cards in the game
            - if the game changer is NO_EXCLUDED_WORDS, the forbidden words are removed
            - the selected card is added into the table of used cards so it cannot be used again in this game
            :return: the selected card
            :rtype: models.Card
        """
        unusedCards = self.round.game.getUnusedCards()
        if len(unusedCards) == 0:
            return None
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
            cardData['card']['forbiddenwords'] = []
        return cardData

    def skip(self):
        """
            - the current card is skipped
            - the team is penalised for skipping if it has exceeded the number of free skips and the UNLIMITED_SKIPS game changer is not selected
        """
        currentCard = self.card
        currentCard.skippedCount += 1
        self.numberOfSkips += 1
        skipPenaltyAfter = self.round.game.skipPenaltyAfter
        if(self.numberOfSkips > skipPenaltyAfter and not(self.gameChangerNumber == UNLIMITED_SKIPS)):
            self.penaliseTeam()

    def awardTeamByID(self,teamID):
        """
            - awards the point to the team for correctly guessing the buzzword
            - the card wonCount is also updated for future card analysis
            :param teamID: the id of the team to be awarded a point, we need teamID when the ALL_GUESSERS game changer has been selected in which any team can be awared a point
            :type teamID: int
        """
        session = globalVars.Session.object_session(self)
        otherTeam = TeamModel.getTeamById(session,teamID)
        self.card.wonCount += 1
        otherTeam.score += 1
        session.commit()

    def awardTeam(self):
        """
            - award the point to the team which is on deck
        """
        session = globalVars.Session.object_session(self)
        self.card.wonCount += 1
        self.team.score += 1
        session.commit()

    def penaliseTeam(self):
        """
            - deducts one point to the team on deck for an infraction
        """
        session = globalVars.Session.object_session(self)
        self.card.lostCount += 1
        self.team.score -= 1
        session.commit()

    def startTimer(self):
        """
            - starts the timer to keep track of the time used in the turn, called when the "Start Turn" button is clicked
            - checks the selected game changer and updates the duration accordingly
            - the timer object is stored in a global, "turnTimers" dictionary for future use during pausing or stopping
            :param callback: the method called when the timer is paused or has expired
            :type callback: "callback method"
        """
        players=self.round.game.getAllPlayers()
        playerEmails = [ player.email for player in players ]
        duration = self.turnDuration
        if( DOUBLE_ROUND_TIME == self.gameChangerNumber ):
            duration*=2
        elif( HALF_ROUND_TIME == self.gameChangerNumber ):
            duration*=.5
        timer = Timer(duration=duration,playerEmails=playerEmails,gameID=self.round.game.id,turnID=self.id)
        globalVars.turnTimers[self.id]=timer
        timer.run()

    def getTimer(self):
        """
            - returns the timer object associated with this turn
            :return: the timer object which keeps track of the time in this turn
            :rtype: threading.Thread
        """
        return globalVars.turnTimers[self.id]

    def removeTimer(self):
        """
            - deletes the timer object when it is no longer needed to free memory
        """
        del globalVars.turnTimers[self.id]

    def __repr__(self):
        """
            - the string representation of the Turn object
        """
        return "<Turn(id:{})>".format(self.id)
