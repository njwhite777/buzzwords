#!/usr/bin/env python
import time
import random
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
    game_changer_number = Column(Integer)
    round_id = Column(Integer, ForeignKey('round.id'), nullable=False)
    card_id = Column(Integer, ForeignKey('card.id'), nullable=True)
    card = relationship("Card", foreign_keys=card_id, lazy = False)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=True)
    # team = relationship("Team", foreign_keys=team_id), causes a backref problem because Team has this reference
    turn_teller_id = Column(Integer, ForeignKey('player.id'), nullable=True)
    turn_moderator_id = Column(Integer, ForeignKey('player.id'), nullable=True)
    teller = relationship('Player', foreign_keys=turn_teller_id )
    moderator = relationship('Player', foreign_keys=turn_moderator_id )

    def __init__(self, number):
        self.number = number
        self.numberOfSkips = 0
        self.startTime = time.time()
        self.game_changer_number = 3
        self.card = None

    def set_team(self, team):
        self.team = team

    def get_teams_not_on_turn(self, game):
        teams_not_on_turn = []
        for the_team in game.teams:
            if self.team.id != the_team.id:
                teams_not_on_turn.append(the_team)
        return teams_not_on_turn

    def get_random_team(self, teams):
        number_of_teams = len(teams_not_on_turn)
        random_team_index = random.randint(0, number_of_teams - 1)
        selected_team = teams_not_on_turn[random_team_index]
        return selected_team

    def get_random_player(self, players):
        players = selected_team.players
        number_of_players = len(players)
        random_player_index = random.randint(0, number_of_players - 1)
        return players[random_player_index]

    def get_random_unused_card(self, cards):
        number_of_cards = len(cards)
        random_card_index = random.randint(0, number_of_cards - 1)
        return cards[random_card_index]

    def set_moderator(self, game):
        teams_not_on_turn = self.get_teams_not_on_turn(game)
        random_team = self.get_random_team(teams_not_on_turn)
        moderator = self.get_random_player(random_team.players)
        moderator.role = 2
        self.moderator = moderator
        return moderator

    def set_teller(self):
        teller = self.get_random_player(self.team.players)
        teller.role = 1
        self.teller = teller
        return teller

    def load_card(self, game):
        unused_cards = game.get_unused_cards()
        if len(unused_cards) == 0:
            return None
        # we might mind to implement a more elegant algorithm which picks a card depending on the stats
        # like number of times gotten right or missed
        card = self.get_random_unused_card()
        self.card = card # sets a new card to the turn
        game.add_used_card(card)
        return card

    def can_skip(self):
        pass


    def __repr__(self):
        return "<GameRound()>".format()
