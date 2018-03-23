#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from . import Base,ForeignKey

class RoundScores(Base):
    __tablename__    = 'roundscores'
    round_id         = Column(Integer,ForeignKey("round.id"))
    team_id          = Column(Integer,ForeignKey("team.id"))
    team_score       = Column(Integer)

    def __repr__(self):
        return "<RoundScores(id='{}',team_id='{}',team_score='{}')>".format(self.id,self.team_id,self.team_score)
