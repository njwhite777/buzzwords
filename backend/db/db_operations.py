#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from argparse import ArgumentParser
# from config import *

parser = ArgumentParser()
parser.add_argument('-c','--create',action='store_true',default=None)
parser.add_argument('-e','--exists',action='store_true',default=None)
parser.add_argument('-m','--mode',default='debug')
parser.add_argument('-x','--delete',action='store_true',default=None)
parser.add_argument('-d','--debug',action='store_true',default=False)
parser.add_argument('-u','--url',default=None)

debug = False

def delete_db(engine):
    if(database_exists(engine.url)):
        drop_database(engine.url)

def create_db(engine):
    if not database_exists(engine.url):
        create_database(engine.url)
    if(debug):
        print(database_exists(engine.url))
    return database_exists(engine.url)

def exists_db(engine):
    if(database_exists(engine.url)):
        if(debug): print("The database {} exists.".format(engine.url))
        return True
    if(debug): print("The database {} does not exist.".format(engine.url))
    return False

def main():
    args = parser.parse_args()
    global debug
    engine = none
    debug = args.debug

    if(args.url):
        engine = create_engine(args.url)
    else:
        engine = create_engine('sqlite:///testdb.db')

    if(args.create):
        create_db(engine)
    elif(args.exists):
        exists_db(engine)
    elif(args.delete):
        delete_db(engine)

if __name__ == '__main__':
    main()
# else:
    # if(config == )
