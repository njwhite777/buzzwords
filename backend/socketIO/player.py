#!/usr/bin/env python
from models import *
import globalVars
import sys
from flask import request
from flask_socketio import emit

# TODO: record the player and associate information with the session ID
@globalVars.socketio.on('player_login',namespace='/io/player')
def playerLogin(data):
    session = globalVars.Session()
    player=PlayerModel.findPlayerByEmail(session,data['email'])
    if(player):
        globalVars.socketIOClients[request.sid] = data['email']
        globalVars.socketIOClients[player.id] = request.sid
        globalVars.socketIOClients[data['email']] = request.sid # storing request.namespace might be a good idea here
    else:
        feedback = PlayerModel.isValidPlayer(data)
        if not feedback['valid']:
            errorMessage = feedback['message']
            return
        player = PlayerModel(data['username'], data['email'], 3)
        session.add(player)
        session.commit()
        globalVars.socketIOClients[request.sid] = data['email']
        globalVars.socketIOClients[player.id] = request.sid
        globalVars.socketIOClients[data['email']] = request.sid
        playerLogin = {
            'username' : player.nickname,
            'email' : player.email,
            'playerID': player.id,
        }
        emit('player_logged_in',playerLogin) # storing request.namespace might be a good idea here
    session.commit()
    session.close()
