#!/usr/bin/env python
from flask import Flask,request
import random, threading, webbrowser

from db import create_app_database,Base
import quizlet
import json
import sys
import globalVars
from models import CardModel

# Next two methods are badly coupled.
# Creates app, applies configuration information, returns
def create_app(app_name=None,environment='dev',configFile=None,config=None):
    if(not(app_name)):
        app_name=__name__
    app=Flask(__name__)

    # Check to see if we should be loading from the config file or
    #  the config file pointed to by the env.
    if(configFile and 'dev_config' in configFile):
        app.config.from_object(configFile['dev_config'])
    if(configFile and 'prod_config' in configFile):
        app.config.from_envvar(configFile['prod_config'],silent=True)

    # TODO: apply any cl parameters that override other things
    if(config):
        pass
    return app

# This method is nigh useless...
def create_db_connection(app,rebuilddb=False):
    if(rebuilddb or 'REBUILDDB' in app.config and app.config['REBUILDDB']):
        rebuilddb = True
    return create_app_database(app.config['DB_URI'],rebuilddb=rebuilddb)

def getQuizletCards(login='Nathan_White34',client_id='SN77uEA94G',endpoint='258934949'):
    # Getting the cards from quizlet.
    session=globalVars.Session()
    quizletClient = quizlet.QuizletClient(client_id=client_id, login=login)
    data = quizletClient.sets.endpoint.get(endpoint)
    count = 0
    for term in data['terms']:
        count+=1
        definitions = term['definition'].split('\n')
        buzzword = term['term'].strip()
        buzzword.split()
        card = CardModel(buzzword=buzzword,forbidden_words=json.dumps(definitions[:-1]),source=definitions[-1],source_page=' '.join(definitions[-1].split()[-2:]),is_phrase=(len(buzzword.split())>1),quizletEndpoint=endpoint)
        session.add(card)
    session.commit()
    session.close()
