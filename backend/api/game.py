#!/usr/bin/env python
from flask import Response, json
from flask_restful import Resource
from models import *

class Game(Resource):

    def __init__(self):
        pass


    def get(self):
        return [
            {'id':10,'name':'blatherStammer','teams':['t1','t2','t3']},
            {'id':11,'name':'textualChallenge','teams':['red','blue','green']},
            {'id':12,'name':'talkTalkTalk','teams':['t1','t2','t3']},
            {'id':13,'name':'fearthebeard','teams':['t1','t2','t3']},
            {'id':13,'name':'whatthe?','teams':['t1','t2','t3']},
            ]



class GameDetails(Resource):

    def __init__(self):
        pass

    def get(self,gameid):
        return {"status":"success"}
