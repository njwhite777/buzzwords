'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:gameService
 * @description
 * # gameService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('gameService',['socketService','debug',function(socketService,debug){
    //
    // This service listens to the created game event and adds a new game to the list when one is created.

    var games;
    var socket = socketService.gameSocket;

    // The event listener which listens for game creation events.
    socket.on('created_game',function(message){
      if(debug) console.log("gameSocket:created_game");
      console.log(message);
      // TODO: add new game to the list of games currently maintained.
    });

    socket.on('deleted_game',function(){
      if(debug) console.log("gameSocket:deleted_game");
      // TODO: remove the game
    });

    return {
      'games' : games
    };

  }]);
