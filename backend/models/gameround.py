#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from . import Base

class GameRound(Base):

    __tablename__ = 'gameround'
    game_id          = Column(Integer,primary_key=True)
    round_id         = Column(Integer,primary_key=True)

    # TODO: what else will we need?

    def __repr__(self):
        return "<GameRound()>".format()
