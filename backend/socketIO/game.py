#!/usr/bin/env python
from models import *
from app import session,socketio
from flask_socketio import emit
from flask import request
import sys


# request_games: returns a list of current and open games on the server
#  list is in the form [{game1info},{game2info},...,{}]
# client must emit on the /io/game namespace:
#  'request_games'
@socketio.on('request_games',namespace='/io/game')
def request_games():
    # TODO: do db operations
    # return the games only to the requesting clients.
    games = [
        {'id':10,'name':'workworkwork','teams':['t1','t2','t3']},
        {'id':11,'name':'textualChallenge','teams':['red','blue','green']},
        {'id':12,'name':'talkTalkTalk','teams':['t1','t2','t3']},
        {'id':13,'name':'fearthebeard','teams':['t1','t2','t3']},
        {'id':13,'name':'?','teams':['t1','t2','t3']},
        ]
    emit('game_list',games)

# validate_game: returns an object that indicates if the game is valid or not.
#  in the form { valid : false }
# client must emit on the /io/game namespace:
#  'validate_game'
@socketio.on('validate_game_config',namespace='/io/game')
def validate_game(data):
    # TODO: returns if the game is valid or not.
    # emits only to the requesting client.
    if(data['_gameValid']):
        emit('show_game_start_button_enabled',{'name':data['name'],'valid':True})
    else:
        emit('show_game_start_button_enabled',{'name':data['name'],'valid':False})


# init_game: once a game is validated, a client should be able to transmit an init_game.
#  once this has happened and the game has been inited in the db,
#  the socket server will have to emit a response on the views channel
#  which tells the game creator's view to switch to the start game view.
#  At this point the game should become visible to all other clients.
#  clients who join get the waiting for game view.
@socketio.on('init_game',namespace='/io/game')
def init_game(data):
    # TODO: gets passed if the game is valid and tbe user has pressed the init game button
    #  time to build the game in the db and tell the creator's view to switch
    # ...
    emit('show_game_start_view',{'game_name':data['name']})

    # This can be emitted to all clients. Tells them a new game has been created.
    #   allows them to update their views.
    emit('created_game', {'data': data['data']},broadcast=True)

# 'validate_game_start': once a game is in a waiting state, joining clients should emit
#  this message.  If the game is indeed ready to start, the server should emit to the starting
#  client that the game is ready to start and the the start game button should become clickable.
@socketio.on('validate_game_start',namespace='/io/game')
def validate_game_start(data):
    emit('show_game_start_button_enabled',{})
