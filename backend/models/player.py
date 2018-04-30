#!/usr/bin/env python
from . import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from constants import TELLER,GUESSER,OBSERVER,MODERATOR
from .validator import *

class Player(Base):
    """
        - the object representation of a taboo player

    	:ivar id: the primary key of the table
    	:ivar nickname: the chosen name of the player, must have between 2 and 255 characters long
    	:ivar email: email of the player which must be unique across the whole system
    	:ivar role: a player can have one of the four roles; teller, moderator, guesser or observer
    	:ivar teamID: a foreign key from the team table to keep track of the team the player belongs to
        :ivar game: used in the game class to enable the game keep a list of all players in the game, initially I found sqlalchemy working this way, I will see if moving this to the game class can still work
    	:ivar turnTeller: used by the Turn class to keep track of the player whose has a "teller role"
        :ivar turnModerator: used by the Turn class to keep track of the player whose has a "moderator role"
	"""
    __tablename__ = 'player'
    id       = Column(Integer,primary_key=True)
    nickname = Column(String(128))
    email = Column(String(128))
    role = Column(Integer)
    teamID = Column(Integer, ForeignKey('team.id'), nullable=True)

    game = relationship("Game",lazy = True, uselist=False)
    turnTeller = relationship("Turn", foreign_keys='Turn.turnTellerId', backref = "turnTeller", lazy = False, uselist=False)
    turnModerator = relationship("Turn", foreign_keys='Turn.turnModeratorId', backref = "turnModerator", lazy = False, uselist=False)

    def __init__(self, nickname, email, role):
        self.nickname = nickname
        self.email = email
        self.role = role
        self.game = None

    @staticmethod
    def numberOfRows(session):
        return session.query(Player).count()
    @staticmethod
    def isValidPlayer(data):
        """
            - validates the form data used for creating the player
            :param data: the key-value pairs of the form data received from the front end
            :type data: dictionary
            :return: the dictionary with key valid = False if not all data is not valid, valid = True if all data is valid
            :rtype: dictionary
        """
        feedback = Validator.isValidPlayer(data)
        return feedback

    @staticmethod
    def emailExists(session, email):
        """
            - checks if the entered email already exists
            :param session: database session
            :type session: sqlalchemy.orm.Session
            :param email: player's email
            :type email: string
            :return: True if the email exists, False otherwise
            :rtype: bool
        """
        player = session.query(Player).filter(Player.email==email).first()
        if(player != None and player.email):
            return player.email
        return False

    @staticmethod
    def findPlayerByEmail(session,email):
        """
            - finds the player by email
            :param session: database session
            :type session: sqlalchemy.orm.Session
            :param email: player's email
            :type email: string
            :return: Player if the player exists, None otherwise
            :rtype: Player
        """
        return session.query(Player).filter(Player.email==email).first()

    @staticmethod
    def findPlayerById(session, id):
        """
            - finds the player by id
            :param session: database session
            :type session: sqlalchemy.orm.Session
            :param id: player's id
            :type id: int
            :return: Player if the player exists, None otherwise
            :rtype: Player
        """
        player = session.query(Player).get(id)
        return player

    def setObserver(self):
        """
            - sets the role of the player to OBSERVER
        """
        self.role = OBSERVER

    def setGuesser(self):
        """
            - sets the role of the player to GUESSER
        """
        self.role = GUESSER

    def setModerator(self):
        """
            - sets the role of the player to MODERATOR
        """
        self.role = MODERATOR

    def setTeller(self):
        """
            - sets the role of the player to TELLER
        """
        self.role = TELLER

    def isObserver(self):
        """
            - checks if the player is an observer
            :return: True if player's role is observer, False otherwise
            :rtype: bool
        """
        return self.role == OBSERVER

    def isGuesser(self):
        """
            - checks if the player is a guesser
            :return: True if player's role is guesser, False otherwise
            :rtype: bool
        """
        return self.role == GUESSER

    def isTeller(self):
        """
            - checks if the player is a teller
            :return: True if player's role is teller, False otherwise
            :rtype: bool
        """
        return self.role == TELLER

    def isModerator(self):
        """
            - checks if the player is a moderator
            :return: True if player's role is moderator, False otherwise
            :rtype: bool
        """
        return self.role == MODERATOR

    def __repr__(self):
        return "<Player(id='{}',name='{}',email='{}')>".format(self.id, self.nickname,self.email)
