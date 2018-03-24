#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship, session
from . import Base

class Card(Base):

    __tablename__ = 'card'
    id          = Column(Integer, primary_key=True)
    buzzword    = Column(String)
    forbidden_words   = Column(String)
    skipped_count = Column(Integer)
    won_count = Column(Integer)
    lost_count = Column(Integer)
    source      = Column(String)
    source_page = Column(String)
    turns = relationship("Turn", backref = "card", lazy = False)

    def __repr__(self):
        return "<Card(id='{}', buzzword='{}', source='{}')>".format(
            self.id, self.buzzword, self.source)
