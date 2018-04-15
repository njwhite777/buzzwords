import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()
from socketIO_client import SocketIO,BaseNamespace,LoggingNamespace



class GameNamespace(BaseNamespace):

    def on_connect(self):
        print('connect game namespace')

    def on_game_list(self,data):
        print("Game List:")
        print(data)


def on_response(data):
    print('I got game result!')
    print(data)

def on_connect():
    print('connect')

def on_disconnect():
    print('disconnect')

def on_reconnect():
    print('reconnect')

def on_aaa_response(*args):
    print('on_aaa_response', args)


socketIO = SocketIO('localhost', 5000)
game_namespace = socketIO.define(GameNamespace, '/io/game')
game_namespace.emit('request_games')
game_namespace.on('game_list',)

# with SocketIO('localhost', 5000, LoggingNamespace) as socketIO:
#     socketIO.emit('request_games')
#     socketIO.wait(seconds=1)
