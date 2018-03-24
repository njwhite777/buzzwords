#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from . import Base

class Player(Base):

    __tablename__ = 'player'
    id       = Column(Integer,primary_key=True)
    nickname           = Column(String)
    email           = Column(String)
    role = Column(Integer)
    game_id = Column(Integer, ForeignKey('game.id'), nullable=True)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=True)
    #turn_teller_id = Column(Integer, ForeignKey('turn.id'), nullable=True)
    #turn_moderator_id = Column(Integer, ForeignKey('turn.id'), nullable=True)

    turnTeller = relationship("Turn", backref = "player", lazy = False, uselist=False)
    turnModerator = relationship("Turn", backref = "player", lazy = False, uselist=False)

    # TODO: what else will we need?
    def __repr__(self):
        return "<Player(id='{}',fname='{}',lname='{}',email='{}',phone='{}')>".format(id,fname,lname,email,phone)
