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
        player = PlayerModel(data['username'], data['email'], 3)
        session.add(player)
        session.flush()
        socketIOClients[request.sid] = data['email']
        socketIOClients[player.id] = request.sid
        socketIOClients[data['email']] = request.sid # storing request.namespace might be a good idea here
    session.commit()
    session.close()

@socketio.on('player_join_team',namespace='/io/player')
def playerJoinTeam(data):
    session = Session()
    playerId = socketIOClients[request.sid]
    player = PlayerModel.findPlayerById(session, playerId)
    if player:
        print("the player does not exist")
        return
    teamId = data['team_id']
    team = TeamModel.findTeamById(session, teamId)
    if team is None:
        print("the team does not exist")
        return
    player.team = team
    session.commit()
    session.close()

    viewData = {'swapView':'gameinitiatorwait'}
    emit('swap_view',viewData,namespace="/io/view")
