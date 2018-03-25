'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:gameService
 * @description
 * # gameService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
.service('socketService',[
  'socketFactory',
  'socketIOConfig',
  function(socketFactory,socketIOConfig) {

    // This is the only way I could figure out to hook up the sockets!
    //  note the port on this is the port of the flask server.
    var IOsocketName = socketIOConfig.getSocketName();
    var gameSocketName = socketIOConfig.getSocketName('game');
    var viewSocketName = socketIOConfig.getSocketName('view');
    var timerSocketName = socketIOConfig.getSocketName('timer');

    var ioSocketConnect = io.connect(IOsocketName);
    var gameSocketConnect = io.connect(gameSocketName);
    var viewSocketConnect = io.connect(viewSocketName);
    var timerSocketConnect = io.connect(timerSocketName);

    var socket = socketFactory({
      ioSocket: ioSocketConnect
    });

    var gameSocket = socketFactory({
      ioSocket: gameSocketConnect
    });

    var viewSocket = socketFactory({
      ioSocket: viewSocketConnect
    });

    var timerSocket = socketFactory({
      ioSocket: timerSocketConnect
    });

    // Connect emitted from server.
    // socket.on('connect',function(){ console.log("socketio connected"); });

    // Disconnect issued by server.
    // socket.on('disconnect',function(message){ console.log(message); });

    return {
      socket: socket,
      gameSocket: gameSocket,
      viewSocket: viewSocket,
      timerSocket: timerSocket
    };

}]);
