#!/usr/bin/env python
from models import *
from app import Session,socketio, socketIOClients
from flask_socketio import emit
from flask import request
import sys
import time


# @socketio.on('starting_turn',namespace='/io/game')
# def start_turn(data):
#     print(data)
