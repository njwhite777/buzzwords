#!/usr/bin/env python
import datetime
from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from . import Base

usedCards = Table('used_cards',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('game.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('card.id'), primary_key=True)
)

class Game(Base):

    __tablename__ = 'game'
    id          = Column(Integer, primary_key=True)
    name = Column(String)
    defaultRoundTime = Column(Integer)
    createdTimeStamp = Column(DateTime, default=datetime.datetime.utcnow)
    initiator_id = Column(Integer, ForeignKey('player.id'), nullable=True)
    initiator = relationship("Player", foreign_keys = initiator_id, lazy = False, uselist=False)
    teams = relationship("Team", backref = "game", lazy = False)
    rounds = relationship("Round", backref = "game", lazy = False)
    used_cards = relationship("Card", secondary=usedCards, lazy = False)

    def __init__(self, name, initiator, defaultRoundTime ):
        self.name = name
        self.defaultRoundTime = defaultRoundTime
        self.initiator = initiator
        self.teams = []
        self.used_cards = []

    def add_used_card(self, card):
        self.used_cards.append(card)

    def set_teams(self, teams):
        self.teams = teams

    def __repr__(self):
        return "<Game(id='{}', player_count='{}', cards_to_win='{}', number_of_teams='{}')>".format(
            self.id,self.player_count,self.cards_to_win,self.number_of_teams)
