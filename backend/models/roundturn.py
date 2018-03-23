#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from . import Base,ForeignKey

class RoundTurn(Base):
    __tablename__ = 'roundturn'
    id = Column(Integer)
    round_id = Column(Integer,ForeignKey("round.id"))
    team_id = Column(Integer,ForeignKey("team.id"))
    turn_order = Column(Integer)
    team_score = Column(Integer)

    # TODO: what else will we need?
    def __repr__(self):
        return "<RoundTurn()>".format()
