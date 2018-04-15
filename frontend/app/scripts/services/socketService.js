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
  '$q',
  'debug',
  function(socketFactory,socketIOConfig,$q,debug) {

    // This is the only way I could figure out to hook up the sockets!
    //  note the port on this is the port of the flask server.
    var IOsocketName = socketIOConfig.getSocketName();
    var gameSocketName = socketIOConfig.getSocketName('game');
    var viewSocketName = socketIOConfig.getSocketName('view');
    var timerSocketName = socketIOConfig.getSocketName('timer');
    var playerSocketName = socketIOConfig.getSocketName('player');
    var cardSocketName = socketIOConfig.getSocketName('card');

    var ioSocketConnect = io.connect(IOsocketName);
    var gameSocketConnect = io.connect(gameSocketName);
    var viewSocketConnect = io.connect(viewSocketName);
    var timerSocketConnect = io.connect(timerSocketName);
    var playerSocketConnect = io.connect(playerSocketName);
    var cardSocketConnect = io.connect(cardSocketName);

    var socket = socketFactory({
      ioSocket: ioSocketConnect
    });

    var gameSocket = socketFactory({
      ioSocket: gameSocketConnect
    });

    var playerSocket = socketFactory({
      ioSocket: playerSocketConnect
    });

    var viewSocket = socketFactory({
      ioSocket: viewSocketConnect
    });

    var timerSocket = socketFactory({
      ioSocket: timerSocketConnect
    });

    var cardSocket = socketFactory({
      ioSocket: cardSocketConnect
    });

    var notifySocketReady = function() {
      var deferred = $q.defer();
      socket.on('connect',function(message){
        if(debug) console.log("socketService:connected socketio");
        deferred.resolve(message);
      });
      return deferred.promise;
    };

    return {
      socket: socket,
      gameSocket: gameSocket,
      viewSocket: viewSocket,
      timerSocket: timerSocket,
      playerSocket: playerSocket,
      notifySocketReady : notifySocketReady,
      cardSocket: cardSocket
    };

}]);
