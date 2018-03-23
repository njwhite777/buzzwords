#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from . import Base

class Roles(Base):
    __tablename__ = 'roles'
    id          = Column(Integer,primary_key=True)
    role_name     = Column(Integer,primary_key=True)
    role_perms    = Column(String)

    # TODO: what else will we need?
    def __repr__(self):
        return "<Roles(id='{}',role_name='{}',role_perms='{}')>".format(id,role_name,role_perms)
