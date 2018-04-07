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
    gameId = Column(Integer, ForeignKey('game.id'), nullable=False)
    turns          = relationship("Turn", lazy = False) # relationship("Turn", backref = "round", lazy = False)
    #game = relationship("Game", foreign_keys=gameId, lazy = False, uselist=False)

    def __init__(self, number):
        self.number = number
        self.turns = []

    def addTurn(self, turn):
        self.turns.append(turn)

    def getLastTurn(self):
        if len(self.turns) == 0:
            return None
        return self.turns[len(self.turns) - 1]


    # TODO: what else will we need?
    def __repr__(self):
        return "<Round(id='{}')>".format(id)
