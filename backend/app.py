#!/usr/bin/env python
from flask import Flask
import random, threading, webbrowser
from flask_restful import Api, Resource
from flask_socketio import SocketIO,emit


from sqlalchemy import create_engine
from db import create_db,delete_db
from sqlalchemy.orm import sessionmaker


#  TODO: will probably want to load the models in the api classes so that they can be manipulated in
#  the api endpoints.
from api import Player,Card,Team,Round,GameTeam,GameRound,Game

from models import Base as AppModelBase
# TODO: This is where the ORM magic happens. Make sure additional classes are
#  created in ./models and imported by __init__.py
from models import *
import argparse
from IPython import embed

parser = argparse.ArgumentParser()
parser.add_argument('-e','--env',default='dev',help="Pass the environment : dev, test, prod")


if __name__ == '__main__':

    args = parser.parse_args()

    app = Flask(__name__)
    api = Api(app)
    socketio = SocketIO(app)


    # SQLite Database for now
    engine = create_engine("sqlite:///db/{}.sqlite".format(args.env))
    create_db(engine)

    # Just want to start the  api service. Don't need to launch the frontend from here.
    #  it is completely decoupled and handled by the grunt serve process for the time being.
    #  Eventually, will just be served by a static server like nginx or apache.
    # port = 5000
    # url = "http://127.0.0.1:{0}".format(port)
    # threading.Timer(1.25, lambda: webbrowser.open(url) ).start()

    # This defines the REST APIs that will be availible.
    api.add_resource(Player, '/player/<int:id>', endpoint = 'player')
    api.add_resource(Card, '/card/<int:id>', endpoint = 'card')
    api.add_resource(Game, '/game/<int:id>', endpoint = 'game')
    api.add_resource(Team, '/team/<int:id>', endpoint = 'team')
    api.add_resource(Round, '/round/<int:id>', endpoint = 'round')


    # This defines the sockets that will be availible.
    @socketio.on('created_game', namespace='/io/game')
    def created_game(message):

        print(message)
        emit('created_game', {'data': message['data']},broadcast=True)


    # SocketIO emits a connect by default.
    # @socketio.on('connect', namespace='/io')
    # def clientConnect():
    #     emit('client_connect', {'data': 'Server: SocketIO Client Connected!'})

    @socketio.on('disconnect', namespace='/io')
    def clientDisconnect():
        print('Server: Socketio Client Disconnected')

    environment = args.env


    if(environment == 'testdb'):
        from models import CardModel

        delete_db(engine)
        AppModelBase.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()



        session.add_all([
            CardModel(buzzword="buzzword1",forbidden_words="{ 'word1':'word','word2':word' }",source="Class Notes",source_page="pg. 5"),
            CardModel(buzzword="buzzword2",forbidden_words="{ 'word1':'word','word2':word' }",source="Class Notes",source_page="pg. 5")
        ])
        session.commit()

        embed()

    if(environment in ['test','debug','dev']):
        delete_db(engine)

    AppModelBase.metadata.create_all(engine)

    socketio.run(app,debug=True,port=5000,host='localhost')
    # app.run(port=port, debug=False)

    # try:
    # except KeyboardInterrupt as e:
    #     print("Keyboard interrupt! Shutting down server.")
