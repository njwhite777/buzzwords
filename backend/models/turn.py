#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from .player import Player
from . import Base

class Turn(Base):

    __tablename__ = 'turn'
    id          = Column(Integer,primary_key=True)
    number         = Column(Integer)
    numberOfSkips = Column(Integer)
    startTime = Column(DateTime)
    round_id = Column(Integer, ForeignKey('round.id'), nullable=False)
    card_id = Column(Integer, ForeignKey('card.id'), nullable=True)
    card = relationship("Card", foreign_keys=card_id, lazy = False)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=True)
    turn_teller_id = Column(Integer, ForeignKey('player.id'), nullable=True)
    turn_moderator_id = Column(Integer, ForeignKey('player.id'), nullable=True)
    teller = relationship('Player', foreign_keys=turn_teller_id )
    moderator = relationship('Player', foreign_keys=turn_moderator_id )


    def __repr__(self):
        return "<GameRound()>".format()
