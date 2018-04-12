from threading import Thread
from app import socketio,socketIOClients
from flask_socketio import emit
import datetime
import time

class Timer(Thread):

    def __init__(self,duration=30,playerEmails=[]):
        Thread.__init__(self)
        self.duration = duration
        self.playerEmails = playerEmails
        self.paused = False
        self.stopped = False
        self.daemon = False
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
                for playerEmail in self.playerEmails:
                    # TODO: set up socketio rooms for games so we can just reference the room and then broadcast to it.
                    self.data['startTime'] = timePretty
                    self.data['countdown'] = self.data['duration'] - self.data['transpired']
                    socketio.emit('update_timer',self.data,room=socketIOClients[playerEmail],namespace="/io/timer")
                time.sleep(1)
                self.data['transpired'] += 1
            if(not(self.paused)):
                self.stop()
        self.data['status'] = 'finished'
        socketio.emit('update_timer',self.data,room=socketIOClients[playerEmail],namespace="/io/timer")


    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True
