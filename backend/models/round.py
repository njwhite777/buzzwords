#!/usr/bin/env python
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from . import Base

class Round(Base):
    """
        - the class representation of a round, a round is complete when each team has played equal number of turns

    	:ivar id: the primary key of the table
    	:ivar number: the ordinal number of the round starting with 0, 1, 2, ...
    	:ivar startTime: the time the round has started
    	:ivar turns: the list of turns every team has played in a round
    	:ivar gameID: a foreign key from the game table to help the game class keep track of all the rounds in the game
	"""

    __tablename__ = 'round'
    id = Column(Integer,primary_key=True)
    number       = Column(Integer)
    startTime = Column(DateTime, default=datetime.datetime.utcnow)
    turns          = relationship("Turn", backref = "round", lazy = False)
    gameId = Column(Integer, ForeignKey('game.id'), nullable=False)

    def __init__(self, number,game):
        self.number = number
        self.turns = []
        self.game = game

    @staticmethod
    def getRoundById(roundID,session):
        return session.query(Round).get(int(roundID))

    def addTurn(self, turn):
        """
            - add a new turn to the round
            :param turn: the new turn object
            :type turn: Turn
            :return: None
        """
        self.turns.append(turn)

    def getCurrentTurn(self):
        """
            - returns the last turn to be added in this round, must ensure the turns are returned in the order they were created
            :return: the last turn to be added to the round, None if the round is new
            :rtype: Turn
        """
        if len(self.turns) == 0:
            return None
        return self.turns[len(self.turns) - 1]

    def __repr__(self):
        """string representaion of the round object"""
        return "<Round(id='{}')>".format(id)
