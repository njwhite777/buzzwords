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
    id   = Column(Integer, primary_key=True)
    name = Column(String)
    gameState = Column(String)
    turnDuration = Column(Integer)
    gameChangers = Column(Integer)
    pointsToWin = Column(Integer)
    maxPlayersPerTeam = Column(Integer)
    numberOfTeams = Column(Integer)
    skipPenaltyAfter = Column(Integer)
    createdTimeStamp = Column(DateTime, default=datetime.datetime.utcnow)
    initiatorID = Column(Integer, ForeignKey('player.id'), nullable=True)

    initiator = relationship("Player", foreign_keys=initiatorID, lazy = False, uselist=False)
    teams = relationship("Team", backref = "game", lazy = False)
    rounds = relationship("Round",backref = "game", lazy = False)
    used_cards = relationship("Card",secondary=usedCards, lazy = False)

    def __init__(self,initiator,name=None,turnDuration=30,numberOfTeams=2,maxPlayersPerTeam=5,pointsToWin=30,skipPenaltyAfter=3,gameChangers=1):
        self.name = name
        self.gameState    = "initialized"
        self.turnDuration = turnDuration
        self.gameChangers = gameChangers
        self.pointsToWin  = pointsToWin
        self.maxPlayersPerTeam = maxPlayersPerTeam
        self.numberOfTeams = numberOfTeams
        self.skipPenaltyAfter = skipPenaltyAfter
        self.initiator = initiator

    @staticmethod
    def number_of_rows(session):
        return session.query(Game).count()

    @staticmethod
    def get_game_by_id(session, game_id):
        game = session.query(Game).get(1)
        return game

    @staticmethod
    def get_all_games(session):
        return session.query(Game).all()

    def add_used_card(self, card):
        self.used_cards.append(card)

    def set_teams(self, teams):
        self.teams = teams

    def add_team(self,team):
        self.teams.append(team)

    def is_game_in_valid_state(self):
        if self.rounds == 0:
            return False
        for team in self.teams:
            if len(team.players) < 2:
                return False
        return True


    def is_game_over(self):
        if not self.has_at_least_one_round():
            return False
        elif self.teams_have_equal_turns():
            return False

    def has_at_least_one_round(self):
        return self.rounds > 0

    def teams_have_equal_turns(self):
        turns = self.teams.number_of_turns()
        for team in self.teams:
            if team.number_of_turns() != turns:
                return False
        return True

    def team_has_reached_threshold():
        pass

    def __repr__(self):
        return "<Game(id='{}', name='{}', pointsToWin='{}')>".format(
            self.id,self.name,self.pointsToWin)
