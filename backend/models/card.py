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
    source_page = Column(String)
    is_phrase = Column(Integer)
    turn = relationship("Turn", lazy = False)

    def __init__(self,buzzword,forbidden_words,source,source_page,skipped_count=0,won_count=0,lost_count=0, is_phrase = 0):
        self.buzzword           = buzzword
        self.forbidden_words    = forbidden_words
        self.skipped_count      = skipped_count
        self.won_count          = won_count
        self.lost_count         = lost_count
        self.source             = source
        self.source_page        = source_page
        self.is_phrase          = is_phrase

    @staticmethod
    def number_of_rows(session):
        return session.query(Card).count()

    @staticmethod
    def find_card_by_id(session, id):
        return session.query(Card).get(id)

    @staticmethod
    def load_card():
        pass

    def __repr__(self):
        return "<Card(id='{}', buzzword='{}', source='{}')>".format(
            self.id, self.buzzword, self.source)
