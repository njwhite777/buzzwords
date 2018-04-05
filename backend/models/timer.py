from flask_socketio import emit
from threading import Thread
from app import socketio,socketIOClients

class Timer(Thread):

    def __init__(self,duration=30,players=[]):
        Thread.__init__(self)
        self.duration = duration
        self.players = players

    def run(self):
        for player in players:
            emit('update_timer',{},room=socketIOClients[player.email],namespace="/io/timer")

    def pause(self):
        pass
