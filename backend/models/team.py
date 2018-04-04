#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from . import Base

class Team(Base):
    __tablename__ = 'team'
    id          = Column(Integer,primary_key=True)
    name        = Column(String)
    score = Column(Integer)
    players = relationship("Player", backref = "team", lazy = False)
    turns = relationship("Turn", backref = "team", lazy = False)
    gameId = Column(Integer, ForeignKey('game.id'), nullable=True)

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turns = []

    def addPlayer(self,player):
        self.players.append(player)

    @staticmethod
    def getTeamById(session, id):
        team = session.query(Team).get(id)
        return team

    def numberOfTurns(self):
        return len(self.turns)

    # TODO: what else will we need?
    def __repr__(self):
        return "<Team(id='{}',team_name='{}')>".format(self.id,self.name)
