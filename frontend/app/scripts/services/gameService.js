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

    var gameServiceData = {};
    gameServiceData.games = [];
    gameServiceData.showGameStartButton = false;

    var socket = socketService.gameSocket;

    //TODO: when this service is initialized, should request a list of games from the API.
    //  game updates come over the games socket.
    //TODO: move the url definition into consts so that it can be in the same file as the
    //  rest of the config stuff

    var validateGameConfig = function(game){
      // This is bad. Introduces temporal coupling...
      gameServiceData._checkGameName = game.name;
      game._gameValid = true;
      socket.emit('validate_game_config',game);
    };



    var playerJoinTeam = function(data){
      socket.emit('validate_game_start',data);
    };

    var initGame = function(){
      socket.emit('init_game',gameServiceData._validatedGame);
    }

    // Gets the game list when a game view that needs it is rendered.
    socketService.notifySocketReady().then(
      function(result){
        socket.emit('request_games');
      },
      function(result){}
    );

    socket.on('show_game_init_button_enabled',function(data){
      if(data.name == gameServiceData._checkGameName){
        gameServiceData.showGameStartButton=true;
        gameServiceData._validatedGame = data;
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
      gameServiceData.games = data;
    });

    // The event listener which listens for game creation events.
    socket.on('created_game',function(data){
      if(debug) console.log("gameSocket:created_game");
      gameServiceData.games.push(data)
    });

    socket.on('players_on_team',function(data){
      var teamID = data['teamID'];
      var count = data['playerCount'];
      console.log(data);
      angular.forEach(gameServiceData.games,function(gameObject){
        angular.forEach(gameObject.teams,function(teamObject){
          if(teamID == teamObject.id){
            Object.assign(teamObject,data)
          }

        });
      });
    });

    socket.on('deleted_game',function(){
      if(debug) console.log("gameSocket:deleted_game");
      // TODO: Remove the game
    });

    return {
      playerJoinTeam : playerJoinTeam,
      gameServiceData : gameServiceData,
      validateGameConfig : validateGameConfig,
      initGame: initGame,
    };

  }]);
