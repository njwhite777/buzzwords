#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from . import Base

class Player(Base):

    __tablename__ = 'player'
    id       = Column(Integer,primary_key=True)
    fname           = Column(String)
    lname           = Column(String)
    email           = Column(String)
    phone           = Column(String)

    # TODO: what else will we need?
    def __repr__(self):
        return "<Player(id='{}',fname='{}',lname='{}',email='{}',phone='{}')>".format(id,fname,lname,email,phone)
