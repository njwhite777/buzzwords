#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from flask import Flask, session as http_session
from sqlalchemy.orm import sessionmaker, relationship
from . import Base
from constants import TELLER,GUESSER,OBSERVER,MODERATOR

class Player(Base):

    __tablename__ = 'player'
    id       = Column(Integer,primary_key=True)
    nickname = Column(String)
    email = Column(String)
    role = Column(Integer)
    teamID = Column(Integer, ForeignKey('team.id'), nullable=True)

    game = relationship("Game",lazy = False, uselist=False)

    turnTeller = relationship("Turn", foreign_keys='Turn.turnTellerId', backref = "turnTeller", lazy = False, uselist=False)
    turnModerator = relationship("Turn", foreign_keys='Turn.turnModeratorId', backref = "turnModerator", lazy = False, uselist=False)

    def __init__(self, nickname, email, role):
        self.nickname = nickname
        self.email = email
        self.role = role
        self.game = None

    @staticmethod
    def emailExists(session, email):
        player = session.query(Player).filter(Player.email==email).first()
        if(player != None and player.email):
            return player.email
        return False

    @staticmethod
    def findPlayerByEmail(session,email):
        return session.query(Player).filter(Player.email==email).first()

    @staticmethod
    def isLoggedIn():
        email = http_session.get('email', None)
        return email is not None

    @staticmethod
    def findPlayerById(session, id):
        player = session.query(Player).get(id)
        return player

    def setObserver(self):
        self.role = OBSERVER

    def setGuesser(self):
        self.role = GUESSER

    def setModerator(self):
        self.role = MODERATOR

    def setTeller(self):
        self.role = TELLER

    def isObserver(self):
        return self.role == OBSERVER

    def isGuesser(self):
        return self.role == GUESSER

    def isTeller(self):
        return self.role == TELLER

    def isModerator(self):
        return self.role == MODERATOR



    # TODO: what else will we need?
    def __repr__(self):
        return "<Player(id='{}',name='{}',email='{}')>".format(self.id, self.nickname,self.email)
