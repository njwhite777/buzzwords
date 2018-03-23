#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from . import Base,ForeignKey

class TeamPlayer(Base):
    __tablename__    = 'teamplayer'
    team_id         = Column(Integer,ForeignKey("team.id"))
    player_id       = Column(Integer,ForeignKey("player.id"))

    # TODO: what else will we need?
    def __repr__(self):
        return "<TeamPlayer()>".format()
