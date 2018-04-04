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
    var gameCreateData = {};

    gameServiceData.games = [];
    gameCreateData.showGameStartButton = false;

    var socket = socketService.gameSocket;

    //TODO: when this service is initialized, should request a list of games from the API.
    //  game updates come over the games socket.
    //TODO: move the url definition into consts so that it can be in the same file as the
    //  rest of the config stuff

    var playerJoinTeam = function(data){
      socket.emit('join_team',data);
    };

    var validateGameStart = function(data){
      socket.emit('validate_game_start',data);
    };

    // Called with every update of for fields.
    var validateGameConfig = function(game){
      gameCreateData.game = game;
      gameCreateData.game._gameValid = true;
      socket.emit('validate_game_config',gameCreateData.game);
    };

    var startGame = function(game){
      socket.emit('start_game',gameCreateData.backendValidatedGame);
    };

    // Gets the game list when a game view that needs it is rendered.
    socketService.notifySocketReady().then(
      function(result){
        socket.emit('request_games');
      },
      function(result){}
    );

    // Handles the event wherein the backend tells us the game is ready to go.
    socket.on('show_game_init_button_enabled',function(data){
      if(data.name == gameCreateData.game.name){
        gameCreateData.showGameStartButton=true;
        gameCreateData.backendValidatedGame=data;
      }
    });

    // Called when player clicks the button to initialize the game
    var initGame = function(){
      socket.emit('init_game',gameCreateData.backendValidatedGame);
    }

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
      if(debug) console.log("created_game",data);
      gameServiceData.games.push(data)
    });

    socket.on('created_your_game',function(data){
      if(gameCreateData.backendValidatedGame.name == data.name){
        console.log("created your game: ",data);
        gameCreateData.backendValidatedGame.gameID = data.id;
      }
    });

    socket.on('players_on_team',function(data){
      var teamID = data['teamID'];
      var count = data['playerCount'];
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
      gameCreateData : gameCreateData,
      validateGameConfig : validateGameConfig,
      validateGameStart : validateGameStart,
      initGame: initGame
    };

  }]);
