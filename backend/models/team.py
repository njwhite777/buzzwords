#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from . import Base

class Team(Base):
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
        self.players.append(player)

    def numPlayers(self):
        return len(self.players)

    def validTeam(self):
        return len(self.players) >= 2

    def teamFull(self):
        return len(self.players) == self.maxPlayersPerTeam

    @staticmethod
    def getTeamById(session, id):
        return session.query(Team).get(id)

    def numberOfTurns(self):
        return len(self.turns)

    # TODO: what else will we need?
    def __repr__(self):
        return "<Team(id='{}',team_name='{}')>".format(self.id,self.name)
