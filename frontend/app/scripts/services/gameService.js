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
    gameData.games = [];
    gameData.showGameStartButton = false;

    var socket = socketService.gameSocket;

    //TODO: when this service is initialized, should request a list of games from the API.
    //  game updates come over the games socket.
    //TODO: move the url definition into consts so that it can be in the same file as the
    //  rest of the config stuff

    var validateGameConfig = function(game){
      // This is bad. Introduces temporal coupling...
      gameData._checkGameName = game.name;
      game._gameValid = true;
      socket.emit('validate_game_config',game);
    };

    // Gets the game list when a game view that needs it is rendered.
    socketService.notifySocketReady().then(
      function(result){
        socket.emit('request_games');
      },
      function(result){}
    );

    socket.on('show_game_start_button_enabled',function(data){
      console.log(data,gameData._checkGameName);
      if(data.name == gameData._checkGameName){
        gameData.showGameStartButton=true;
      }
    });

    // On a disconnect from the server set up a listener to notify when then
    //  socket is back up. When it is, request games.
    socket.on('disconnect',function(){
      if(debug) console.log("gameService:disconnected from socket");
      socketService.notifySocketReady().then(
        function(result){
          socket.emit('request_games');
        },
        function(result){
          console.log(result);
        }
      );
    });

    socket.on('game_list',function(data){
      if(debug) console.log("games list",data);
      gameData.games = data;
    });

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
      gameData : gameData,
      validateGameConfig : validateGameConfig,
    };

  }]);
