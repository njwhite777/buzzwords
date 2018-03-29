#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from . import Base

class Team(Base):
    __tablename__ = 'team'
    id          = Column(Integer,primary_key=True)
    team_name        = Column(String)
    score = Column(Integer)
    members = relationship("Player", backref = "team", lazy = False)
    turns = relationship("Turn", backref = "team", lazy = False)
    game_id = Column(Integer, ForeignKey('game.id'), nullable=True)

    def __init__(self, team_name):
        self.team_name = team_name
        self.score = 0
        self.members = []
        self.turns = []

    def add_member(self, member):
        self.members.append(member)

    # TODO: what else will we need?
    def __repr__(self):
        return "<Team(id='{}',team_name='{}')>".format(self.id,self.team_name)
