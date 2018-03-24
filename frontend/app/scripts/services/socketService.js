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

    var ioSocketConnect = io.connect( IOsocketName );
    var gameSocketConnect = io.connect(gameSocketName);

    var socket = socketFactory({
      ioSocket: ioSocketConnect
    });

    var gameSocket = socketFactory({
      ioSocket: gameSocketConnect
    });

    // Connect emitted from server.
    // Should be connected.
    // socket.on('connect',function(){ console.log("socketio connected"); });

    // Disconnect issued by server.
    // socket.on('disconnect',function(message){ console.log(message); });

    return {
      socket : socket,
      gameSocket :  gameSocket
    };

}]);
