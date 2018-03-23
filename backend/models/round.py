#!/usr/bin/env python
from sqlalchemy import Column, Integer, String

class Round(Base):
    __tablename__ = 'round'
    id = Column(Integer,primary_key=True)
    team_id          = Column(Integer,primary_key=True)
    team_score       = Column(Integer)
    round_modifier   = Column(String)

    # TODO: what else will we need?
    def __repr__(self):
        return "<Round(id='{}',team_id='{}',team_score='{}',round_modifier='{}')>".format(id,team_id,team_score,round_modifier)
