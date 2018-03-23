#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from . import Base

class Card(Base):

    __tablename__ = 'card'
    id          = Column(Integer, primary_key=True)
    buzzword    = Column(String)
    json_data   = Column(String)
    source      = Column(String)
    source_page = Column(String)

    def __repr__(self):
        return "<Card(id='{}', buzzword='{}', source='{}')>".format(
            self.id, self.buzzword, self.source)
