#!/usr/bin/env python
import argparse
from flask_cors import CORS
from tests import *
from flask_socketio import SocketIO
import globalVars
from app import create_app,create_db_connection,getQuizletCards


environment = 'prod'

app = create_app(app_name="buzzwords",environment=environment,configFile={ 'dev_config' : 'settings','prod_config':'CS690_SETTINGS'},config={})
globalVars.socketio=SocketIO(app)
globalVars.Session,globalVars.engine = create_db_connection(app,rebuilddb=False)

if(environment == 'dev'):
        getQuizletCards()

from socketIO import *
CORS(app)
