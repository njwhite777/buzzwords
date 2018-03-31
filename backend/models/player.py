#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from flask import Flask, session as http_session
from sqlalchemy.orm import sessionmaker, relationship
from . import Base

class Player(Base):

    __tablename__ = 'player'
    id       = Column(Integer,primary_key=True)
    nickname           = Column(String)
    email           = Column(String)
    role = Column(Integer)
    game = relationship("Game", lazy = False, uselist=False)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=True)
    turnTeller = relationship("Turn", foreign_keys='Turn.turn_teller_id', backref = "turnTeller", lazy = False, uselist=False)
    turnModerator = relationship("Turn", foreign_keys='Turn.turn_moderator_id', backref = "turnModerator", lazy = False, uselist=False)

    def __init__(self, nickname, email, role):
        self.nickname = nickname
        self.email = email
        self.role = role
        self.game = None

    @staticmethod
    def email_exists(session, the_email):
        player = session.query(Player).filter(Player.email==the_email).first()
        return player is not None

    @staticmethod
    def is_logged_in():
        email = http_session.get('email', None)
        return email is not None

    @staticmethod
    def find_player_by_id(session, id):
        player = session.query(Player).get(id)
        return player

    def login(self):
        http_session['email'] = self.email
        http_session['player_id'] = self.id

    def add_team_session(self):
        http_session['team_id'] = self.team.id



    # TODO: what else will we need?
    def __repr__(self):
        return "<Player(id='{}',name='{}',email='{}')>".format(self.id, self.nickname,self.email)
