#!/usr/bin/env python
from flask import Flask,request
import random, threading, webbrowser
from flask_restful import Api, Resource
from flask_socketio import SocketIO,emit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# TODO: there is still more restructuring to happen.
from db import create_db
# TODO: This is where the ORM magic happens. Make sure additional classes are
#  created in ./models and imported by __init__.py
import argparse
import sys
from IPython import embed


app = Flask(__name__)
socketio = SocketIO(app)

#
# TODO: more db setup based on the env that gets passed in.
engine = create_engine("sqlite:///db/{}.sqlite".format("dev"))
create_db(engine)
Session = sessionmaker(bind=engine)
session = Session()
socketIOClients = dict()

# Game Status Constants
GAME_CREATED = 1 # the game has been created but is not ready / valid to start
GAME_READY = 2 # the game can be started
GAME_PLAYING = 3 # the game has been started and is in playing mode
GAME_PAUSED = 4 # the game has been paused
GAME_COMPLETE = 5 # the game is over

# Player roles constants
TELLER = 1
MODERATOR = 2
GUESSER = 3
OBSERVER = 4 # if to be considered, player who is neither the moderator nor the teller and his team is not on deck
