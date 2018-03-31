#!/usr/bin/env python
from models import *
from app import Session,socketio,socketIOClients
import sys
from flask import request

# TODO: record the player and associate information with the session ID
@socketio.on('player_login',namespace='/io/player')
def playerLogin(data):
    print(request.namespace, file=sys.stderr)
    print(request.sid,file=sys.stderr)
    print(data, file=sys.stderr)
    session = Session()
    print("the username is: " + str(data['username']))
    email = str("ron20@gmail.com")
    if PlayerModel.email_exists(session, email):
        print ("the entered email already exists")
    else:
        player = PlayerModel("ron20", email, 3)
        session.add(player)
        session.commit()
        print ("account created")
        socketIOClients[request.sid] = player
        socketIOClients[data['email']] = player
    session.close()
