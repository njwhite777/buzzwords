from threading import Thread
from app import socketio,socketIOClients
from flask_socketio import emit
import datetime
import time
# from socketIO.game import timer_notify_turn_complete

class Timer(Thread):

    def __init__(self,duration=30,playerEmails=[],gameID=None):
        Thread.__init__(self)
        self.duration = duration
        self.playerEmails = playerEmails
        self.paused = False
        self.stopped = False
        self.daemon = True
        self.gameID = gameID
        self.data = {
            'startTime': None,
            'duration': self.duration,
            'countdown': self.duration,
            'transpired': 0,
            'status': 'running'
        }

    def run(self):
        now = datetime.datetime.now()
        timePretty = now.strftime("%Y-%m-%d %H:%M:%S");

        while( not(self.stopped) ):
            while( self.data['countdown'] > 0 and not(self.paused) ):
                if(self.data['status'] == 'paused'):
                    self.data['status'] = 'running'
                    for playerEmail in self.playerEmails:
                        socketio.emit('timer_resumed',self.data,room=socketIOClients[playerEmail],namespace="/io/timer")

                for playerEmail in self.playerEmails:
                    # TODO: set up socketio rooms for games so we can just reference the room and then broadcast to it.
                    self.data['startTime'] = timePretty
                    self.data['countdown'] = self.data['duration'] - self.data['transpired']
                    socketio.emit('update_timer',self.data,room=socketIOClients[playerEmail],namespace="/io/timer")
                time.sleep(1)
                self.data['transpired'] += 1
            if(not(self.paused)):
                self.stop()
            else:
                if(not(self.data['status'] == 'paused')):
                    self.data['status'] = 'paused'
                    for playerEmail in self.playerEmails:
                        socketio.emit('timer_paused',self.data,room=socketIOClients[playerEmail],namespace="/io/timer")

            time.sleep(.5)
        self.data['status'] = 'finished'
        socketio.emit('update_timer',self.data,room=socketIOClients[playerEmail],namespace="/io/timer")
        timer_notify_turn_complete( { 'gameID' : self.gameID } )

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True
