#!/usr/bin/env python
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from . import Base

class Round(Base):
    __tablename__ = 'round'
    id = Column(Integer,primary_key=True)
    number       = Column(Integer)
    startTime = Column(DateTime, default=datetime.datetime.utcnow)
    turns          = relationship("Turn", lazy = False) # relationship("Turn", backref = "round", lazy = False)

    gameId = Column(Integer, ForeignKey('game.id'), nullable=False)
    # Don't need to do this round.game should already exist because of abckref
    # game = relationship("Game", foreign_keys=gameId, lazy = False, uselist=False)

    def __init__(self, number,game):
        self.number = number
        self.turns = []
        self.game = game

    def addTurn(self, turn):
        self.turns.append(turn)

    def getLastTurn(self):
        if len(self.turns) == 0:
            return None
        return self.turns[len(self.turns) - 1]

    def getCurrentTurn(self):
        if len(self.turns) == 0:
            return None
        return self.turns[len(self.turns) - 1]


    # TODO: what else will we need?
    def __repr__(self):
        return "<Round(id='{}')>".format(id)
