'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:gameService
 * @description
 * # gameService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('gameService',['socketService','$http','debug',function(socketService,$http,debug){
    // This service listens to the created game event and adds a new game to the list when one is created.

    if(debug) console.log("game Service!");

    var gameData = {};
    gameData['games'] = [];
    var socket = socketService.gameSocket;

    //TODO: when this service is initialized, should request a list of games from the API.
    //  game updates come over the games socket.
    //TODO: move the url definition into consts so that it can be in the same file as the
    //  rest of the config stuff.

    $http({
      method: 'GET',
      url: 'http://localhost:5000/game'
    }).then(function successCallback(response) {
      if(response.status == 200){
        if(debug) console.log(response.status);
        gameData.games = response.data;
      }
    }, function errorCallback(response) {});

    // The event listener which listens for game creation events.
    socket.on('created_game',function(message){
      if(debug) console.log("gameSocket:created_game");
      console.log(message);
      // TODO: add new game to the list of games currently maintained.
      // gameData.games.push()
    });

    socket.on('deleted_game',function(){
      if(debug) console.log("gameSocket:deleted_game");
      // TODO: remove the game
      //
    });

    return {
      'gameData' : gameData
    };

  }]);
