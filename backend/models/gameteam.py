#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from . import Base,ForeignKey

class GameTeam(Base):

    __tablename__ = 'gameteam'
    game_id         = Column(Integer,ForeignKey("game.id"))
    team_id         = Column(Integer,ForeignKey("team.id"))
    player_id       = Column(Integer,ForeignKey("player.id"))
    team_name       = Column(String)
    team_count      = Column(Integer)

    # TODO: what else will we need?
    def __repr__(self):
        return "<GameTeam()>".format()
