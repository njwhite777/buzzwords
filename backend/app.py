#!/usr/bin/env python
from flask import Flask,request
import random, threading, webbrowser
from flask_restful import Api, Resource
from flask_socketio import SocketIO,emit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base as AppModelBase,CardModel
from db import create_db
import argparse
import sys

app = Flask(__name__)
app.config.from_object('settings')
app.config.from_envvar('CS690_SETTINGS',silent=True)
debug=app.config['DEBUG']
socketio = SocketIO(app)
#
# TODO: more db setup based on the env that gets passed in.
engine=None
if(app.config['ENVIRONMENT'] == 'dev'):
    print("RUNNING IN DEV")
    engine = create_engine(app.config['DB_URI'])
    if(app.config['REBUILDDB']):
        create_db(engine)
        AppModelBase.metadata.create_all(engine)
elif(app.config['ENVIRONMENT'] == 'prod'):
    engine = create_engine(app.config['DB_URI'].format(app.config['DBNAME']))
else:
    pass
    # engine = create_engine(app.config['DB_URI'].format(app.config['DBNAME']))
    # Test

Session = sessionmaker(bind=engine)
session = Session()
socketIOClients = dict()
turnTimers = dict()

def getQuizletCards(login='Nathan_White34',client_id='SN77uEA94G',endpoint='258934949'):
    # Getting the cards from quizlet.
    session=Session()
    quizletClient = quizlet.QuizletClient(client_id=client_id, login=login)
    data = quizletClient.sets.endpoint.get(endpoint)
    count = 0
    for term in data['terms']:
        count+=1
        definitions = term['definition'].split('\n')
        buzzword = term['term'].strip()
        buzzword.split()
        card = CardModel(buzzword=buzzword,forbidden_words=json.dumps(definitions[:-1]),source=definitions[-1],source_page=' '.join(definitions[-1].split()[-2:]),is_phrase=(len(buzzword.split())>1),quizleEndpoint=endpoint)
        session.add(card)
    session.commit()
    session.close()
