#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from . import Base

class Game(Base):

    __tablename__ = 'game'
    id          = Column(Integer, primary_key=True)
    number_of_teams= Column(String)
    cards_to_win= Column(String)
    player_count= Column(String)
    # TODO: what else will we need?

    def __repr__(self):
        return "<Game(id='{}', player_count='{}', cards_to_win='{}', number_of_teams='{}')>".format(
            self.id,self.player_count,self.cards_to_win,self.number_of_teams)
