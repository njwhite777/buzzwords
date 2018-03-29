#!/usr/bin/env python

from app import session,socketio
import sys
from flask import request

# TODO: record the player and associate information with the session ID
@socketio.on('player_login',namespace='/io/player')
def playerLogin(data):
    print(request.namespace, file=sys.stderr)
    print(request.sid,file=sys.stderr)
    print(data, file=sys.stderr)
    # socketIOClients.append(request.namespace)
