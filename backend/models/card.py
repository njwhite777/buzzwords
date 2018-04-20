#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship, session
from . import Base

class Card(Base):

    __tablename__ = 'card'
    id          = Column(Integer, primary_key=True)
    buzzword    = Column(String)
    forbiddenWords   = Column(String)
    skippedCount = Column(Integer)
    quizletEndpoint = Column(String)
    wonCount = Column(Integer)
    lostCount = Column(Integer)
    source      = Column(String)
    sourcePage = Column(String)
    isPhrase = Column(Integer)

    def __init__(self,buzzword,forbidden_words,source,source_page,skipped_count=0,won_count=0,lost_count=0, is_phrase = 0,quizletEndpoint=None):
        self.buzzword           = buzzword
        self.forbiddenWords    = forbidden_words
        self.skippedCount      = skipped_count
        self.wonCount          = won_count
        self.lostCount         = lost_count
        self.source             = source
        self.sourcePage        = source_page
        self.isPhrase          = is_phrase
        self.quizletEndpoint   = quizletEndpoint

    @staticmethod
    def numberOfRows(session):
        return session.query(Card).count()

    @staticmethod
    def findCardById(session, id):
        return session.query(Card).get(id)

    def removeForbiddenWords(self):
        self.forbiddenWords = ""

    def __repr__(self):
        return "<Card(id='{}', buzzword='{}', source='{}')>".format(
            self.id, self.buzzword, self.source)
