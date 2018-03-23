#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from . import Base,ForeignKey

class RoundRoles(Base):

    __tablename__ = 'roundroles'
    round_id         = Column(Integer,ForeignKey("round.id"))
    player_id        = Column(Integer,ForeignKey("player.id"))
    role_id          = Column(Integer,ForeignKey("roles.id"))
    round_turn_order = Column(Integer)

    # TODO: what else will we need?
    def __repr__(self):
        return "<RoundRoles()>".format()
