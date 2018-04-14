import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()
from socketIO_client import SocketIO, LoggingNamespace

with SocketIO('localhost', 5000, LoggingNamespace) as socketIO:
    socketIO.emit("aaa")
    socketIO.wait()
