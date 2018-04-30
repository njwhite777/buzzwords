#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship, session
from . import Base
import random
import globalVars

class Card(Base):
    """
        - the class representation of a card

	:ivar id: the primary key of the table
	:ivar buzzword: the word the teller has to explain to his team for guessing
	:ivar forbiddenWords: list of words the teller can't use unless the word has been said by the guesser first, stored as a json array
	:ivar skippedCount: the number of times the card has been skipped to keep track of the card relevance
	:ivar wonCount: the number of times the card has been gotten right, same role as skippedCount
    :ivar lostCount: the number of times the word couldn't been won, doesn't include skipping, same role as skippedCount
	:ivar source: where the buzzword was found, either text book or notes (the handouts provided in class)
    :ivar sourcePage: the page in the handouts or text book where the buzzword was found
    :ivar isPhrase: a boolean value which is True if the buzzword consists of more than one word
	"""

    __tablename__ = 'card'
    id          = Column(Integer, primary_key=True)
    buzzword    = Column(String(128))
    forbiddenWords   = Column(String(128))
    skippedCount = Column(Integer)
    quizletEndpoint = Column(String(128))
    wonCount = Column(Integer)
    lostCount = Column(Integer)
    source      = Column(String(128))
    sourcePage = Column(String(128))
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
        """
            - finds the number of cards in the card table
            :param session: the database session
            :type session: sqlalchemy.orm.Session
            :return: the number of cards in the table
            :rtype: int
        """
        return session.query(Card).count()

    @staticmethod
    def findCardById(session, id):
        """
            - finds a card by its primary key
            :param session: the database session
            :type session: sqlalchemy.orm.Session
            :return: the card object
            :rtype: Card
        """
        return session.query(Card).get(id)

    @staticmethod
    def getRandomizeCardIds():
        # numberOfCards = Card.numberOfRows(session) # can't think of any easy way of passing the session, hardcoding to 200
        numberOfCards = 200
        allIds = []
        randomizedIds = []
        for i in range(1, numberOfCards + 1):
            allIds.append(i)
        for i in range(0, numberOfCards):
            index = random.randint(0, numberOfCards - i - 1)
            randomizedIds.append(allIds[index])
            allIds.remove(allIds[index])
        return randomizedIds

    def removeForbiddenWords(self):
        """removes forbidden words from the card, used when "NO_FORBIDDEN_WORDS" game changer has been selected"""
        self.forbiddenWords = ""

    def __repr__(self):
        """ string representaion of a card object """
        return "<Card(id='{}', buzzword='{}', source='{}')>".format(
            self.id, self.buzzword, self.source)
