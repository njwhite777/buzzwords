#!/usr/bin/env python
from models import *
from app import session,socketio

# This defines the sockets that will be availible.
def update_timer(message):
    print(message)
    emit('update_timer', {'data': message['data']},broadcast=True)
