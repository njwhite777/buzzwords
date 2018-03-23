#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from . import Base

class Team(Base):
    __tablename__ = 'Team'
    id          = Column(Integer,primary_key=True)
    team_name        = Column(String)

    # TODO: what else will we need?
    def __repr__(self):
        return "<Team(id='{}',team_name='{}')>".format(self.id,self.team_name)
