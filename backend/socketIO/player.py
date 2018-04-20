#!/usr/bin/env python
from models import *
from app import Session,socketio,socketIOClients
import sys
from flask import request

# TODO: record the player and associate information with the session ID
@socketio.on('player_login',namespace='/io/player')
def playerLogin(data):
    session = Session()
    player=PlayerModel.findPlayerByEmail(session,data['email'])
    if(player):
        socketIOClients[request.sid] = data['email']
        socketIOClients[player.id] = request.sid
        socketIOClients[data['email']] = request.sid # storing request.namespace might be a good idea here
    else:
        feedback = PlayerModel.isValidPlayer(data)
        if not feedback['valid']:
            errorMessage = feedback['message']
            return
        player = PlayerModel(data['username'], data['email'], 3)
        session.add(player)
        session.flush()
        socketIOClients[request.sid] = data['email']
        socketIOClients[player.id] = request.sid
        socketIOClients[data['email']] = request.sid # storing request.namespace might be a good idea here
    session.commit()
    session.close()
