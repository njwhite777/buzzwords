#!/usr/bin/env python
from models import *
from app import session,socketio
from flask_socketio import emit

# This defines the sockets that will be availible.
@socketio.on('created_game', namespace='/io/game')
def created_game(message):
    # TODO: verify that this works!
    emit('created_game', {'data': message['data']},broadcast=True)

@socketio.on('request_games',namespace='/io/game')
def request_games():
    # TODO: do db operations
    # return the games only to the requesting clients.
    games = [
        {'id':10,'name':'blatherStammer','teams':['t1','t2','t3']},
        {'id':11,'name':'textualChallenge','teams':['red','blue','green']},
        {'id':12,'name':'talkTalkTalk','teams':['t1','t2','t3']},
        {'id':13,'name':'fearthebeard','teams':['t1','t2','t3']},
        {'id':13,'name':'whatthe?','teams':['t1','t2','t3']},
        ]
    emit('game_list',games)

@socketio.on('validate_game',namespace='/io/game')
def validate_game(data):
    # TODO: returns if the game is valid or not.
    # emits only to the requesting client.
    pass

@socketio.on('init_game',namespace='/io/game')
def init_game(message):
    # TODO: gets passed if the game is valid and tbe user has pressed the init game button
    pass
