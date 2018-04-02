#!/usr/bin/env python
from models import *
from app import Session,socketio,socketIOClients
import sys
from flask import request

# TODO: record the player and associate information with the session ID
@socketio.on('player_login',namespace='/io/player')
def playerLogin(data):
    session = Session()
    player=PlayerModel.find_player_by_email(session,data['email'])
    if(player):
        socketIOClients[request.sid] = player.id
        socketIOClients[data['email']] = player.id # storing request.namespace might be a good idea here
    else:
        player = PlayerModel(data['username'], data['email'], 3)
        session.add(player)
        session.flush()
        socketIOClients[request.sid] = player.id
        socketIOClients[data['email']] = player.id # storing request.namespace might be a good idea here
    session.commit()
    session.close()

@socketio.on('player_join_team',namespace='/io/player')
def playerJoinTeam(data):
    session = Session()
    player_id = socketIOClients[request.sid]
    player = PlayerModel.find_player_by_id(session, player_id)
    if player is None:
        print("the player does not exist")
        return
    team_id = data['team_id'] # should come from the client
    team = TeamModel.find_team_by_id(session, team_id)
    if team is None:
        print("the team does not exist")
        return
    player.team = team
    session.commit()
    session.close()

    viewData = {'swapView':'gameinitiatorwait'}
    emit('swap_view',viewData,namespace="/io/view")
