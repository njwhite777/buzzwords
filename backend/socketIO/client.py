#!/usr/bin/env python
from app import socketio
import sys
from flask import request

# SocketIO emits a connect by default.
@socketio.on('connect', namespace='/io')
def clientConnect():
    # print(request.namespace, file=sys.stderr)
    emit('client_connect', {'data': 'Server: SocketIO Client Connected!'})

@socketio.on('disconnect', namespace='/io')
def clientDisconnect():
    print('Server: Socketio Client Disconnected')
