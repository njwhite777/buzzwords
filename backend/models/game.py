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
    game_changers_activated = Column(Integer)
    game_state = Column(Integer)
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
        self.game_state = 0
        self.teams = []
        self.used_cards = []
        self.rounds = []

    @staticmethod
    def number_of_rows(session):
        return session.query(Game).count()

    @staticmethod
    def get_game_by_id(session, game_id):
        game = session.query(Game).get(1)
        return game

    @staticmethod
    def get_all_games(session):
        games = session.query(Game).all()
        return games

    def add_used_card(self, card):
        self.used_cards.append(card)

    def set_teams(self, teams):
        self.teams = teams

    def is_game_in_valid_state(self):
        if self.rounds == 0:
            return False
        for team in self.teams:
            if len(team.members) < 2:
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
        return "<Game(id='{}', player_count='{}', cards_to_win='{}', number_of_teams='{}')>".format(
            self.id,self.player_count,self.cards_to_win,self.number_of_teams)
