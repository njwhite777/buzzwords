#!/usr/bin/env python
from models import *
from app import session,socketio
import sys
from flask import request

# TODO: record the player and associate information with the session ID
@socketio.on('player_login',namespace='/io/player')
def playerLogin(data):
    print(request.namespace, file=sys.stderr)
    print(request.sid,file=sys.stderr)
    print(data, file=sys.stderr)
    print("the username is: " + str(data['username']))
    email = str(data['email'])
    if PlayerModel.email_exists(session, email):
        print ("the entered email already exists")
    else:
        player = PlayerModel(str(data['username']), email, 3)
        session.add(player)
        session.commit()
        print ("account created")
        player.login()
    # socketIOClients.append(request.namespace)
