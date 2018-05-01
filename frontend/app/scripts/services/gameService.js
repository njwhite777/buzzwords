'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:gameService
 * @description
 * # gameService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('gameService',['socketService','$http','currentGameService','$rootScope','debug',function(socketService,$http,currentGameService,$rootScope,debug){
    // This service listens to the created game event and adds a new game to the list when one is created.

    var games = {};
    var gameCreateData = {};

    gameCreateData.showGameStartButton = false;

    var socket = socketService.gameSocket;

    // Handles joining a team for a client.
    var playerJoinTeam = function(data){
      socket.emit('join_team',data);
    };

    // Called with every update of for fields.
    var validateGameConfig = function(game){
      gameCreateData.game = game;
      socket.emit('validate_game_config',gameCreateData.game);
    };

    // Called as soon as a game is started in the  backend. Removes the game matching this id.
    socket.on('game_started',function(data){
        var gameID = data['gameID'];
        delete games[gameID];
    });

    // Gets the game list when a game view that needs it is rendered.
    socketService.notifySocketReady().then(
      function(result){
        socket.emit('request_games');
      },
      function(result){}
    );

    // #############################################################
    // Game initialization:
    // Handles the event wherein the backend tells us the game is ready to be initialized.
    socket.on('show_game_init_button_enabled',function(data){
      // Must get the game name here
      if(data.name == gameCreateData.game.name){
        console.log("HERE!!!",data);
        gameCreateData.showGameStartButton=true;
        gameCreateData.backendValidatedGame=data;
      }else{
        gameCreateData.showGameStartButton=false;
        $rootScope.$emit('invalid_game_message',data);
      }
    });

    // Called when player clicks the button to initialize the game
    var initGame = function() {
      socket.emit('init_game',gameCreateData.backendValidatedGame);
    }
    // #############################################################

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
      angular.forEach(data,function(gameDetails,idx){
        games[idx] = gameDetails;
      });
    });

    // The event listener which listens for game creation events.
    socket.on('created_game',function(data){
      angular.forEach(data,function(gameDetails,idx){
        games[idx] = gameDetails;
      });
    });

    socket.on('players_on_team',function(data){
      var teamID = data['teamID'];
      var count = data['playerCount'];
      angular.forEach(data,function(gameObject,oIdx){
        angular.forEach(gameObject.teams,function(teamObject,idx){
          Object.assign(games[oIdx].teams[idx],teamObject);
        });
      });
    });

    return {
      playerJoinTeam : playerJoinTeam,
      games : games,
      gameCreateData : gameCreateData,
      validateGameConfig : validateGameConfig,
      initGame: initGame
    };

  }]);
