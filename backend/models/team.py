#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from . import Base

class Team(Base):
    """
        - the object representation of a team

    	:ivar id: the primary key of the table
    	:ivar name: the name of the team
    	:ivar maxPlayersPerTeam: the maximum number of players that can join the team
    	:ivar score: the score of the team, starts at zeroand incremented by one for each card won, decremented by one for any infraction
    	:ivar players: the list of players who are the members of the team
        :ivar turns: the list of turns played by the team
        :ivar gameId: the foreign key of the game to help the game class keep track of all the teams in the game
	"""
    __tablename__ = 'team'
    id          = Column(Integer,primary_key=True)
    name        = Column(String(256))
    maxPlayersPerTeam=Column(Integer)
    score = Column(Integer)
    players = relationship("Player", backref = "team", lazy = False)
    turns = relationship("Turn", backref = "team", lazy = False)
    gameId = Column(Integer, ForeignKey('game.id'), nullable=True)

    def __init__(self, name,maxPlayersPerTeam=5):
        self.name = name
        self.score = 0
        self.maxPlayersPerTeam=maxPlayersPerTeam
        self.turns = []

    def addPlayer(self,player):
        """
            - add a new player in the team
            :param player: the player joining the team
            :type player: Player
            :return: None
        """
        self.players.append(player)

    def numPlayers(self):
        """
            - returns the number of players in the team
            :return: the number of players in the team
            :rtype: int
        """
        return len(self.players)

    def validTeam(self):
        """
            - checks the minimum requirement for an acceptable number of players in a team
            :return: True if the team has at least 2 members, False otherwise
            :rtype: bool
        """
        return len(self.players) >= 2

    def teamFull(self):
        """
            - checks if the team has reached a maximum number of allowed players
            :return: True if team has reached a maximum number of allowed players, False otherwsie
            :rtype: bool
        """
        return len(self.players) == self.maxPlayersPerTeam

    @staticmethod
    def getTeamById(session, id):
        """
            - finds the team by its id
            :param session: the database session
            :type session: sqlalchemy.orm.Session
            :param id: the id of the team
            :type id: int
            :return: the team object, None if the id doesn't exist
            :rtype: Team
        """
        return session.query(Team).get(id)

    def numberOfTurns(self):
        """
            - returns the number of turns the team has played so far
            :return: the number of turns the team has played so far
            :rtype: int
        """
        return len(self.turns)

    def __repr__(self):
        """string representaion of the team object"""
        return "<Team(id='{}',team_name='{}')>".format(self.id,self.name)
