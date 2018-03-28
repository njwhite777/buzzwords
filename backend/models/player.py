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
    initiator = relationship("Game", lazy = False, uselist=False)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=True)
    turnTeller = relationship("Turn", foreign_keys='Turn.turn_teller_id', backref = "turnTeller", lazy = False, uselist=False)
    turnModerator = relationship("Turn", foreign_keys='Turn.turn_moderator_id', backref = "turnModerator", lazy = False, uselist=False)

    def __init__(self, nickname, email, role):
        self.nickname = nickname
        self.email = email
        self.role = role


    # TODO: what else will we need?
    def __repr__(self):
        return "<Player(id='{}',fname='{}',lname='{}',email='{}',phone='{}')>".format(id,fname,lname,email,phone)
