'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:gameService
 * @description
 * # gameService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('currentGameService',['$q','socketService','debug',function( $q,socketService,debug ){

    var socket = socketService.gameSocket;
    var currentGame = {

    };

    var currentTurn = {
      roles:    {},
      team:     {},
      modifier: {}
    };

    var deferred = $q.defer();

    var startGame = function(){
      socket.emit('start_game',currentGame);
    };

    var startTurn = function(){
      socket.emit("starting_turn",currentGame);
    };

    // The event listener which returns when your own game has been created.
    socket.on('created_your_game',function(data){
      setGame(data);
    });

    socket.on('joined_team',function(data){
      setGame(data);
    });

    // Sets the current game and resolves it imediately.
    var setGame = function(game){
      console.log("SETTING GAME:",game)
      console.log("CURRENT GAME:",currentGame)
      Object.assign(currentGame,game);
      deferred.resolve(game);
    }

    var getGame = function(){
      return deferred.promise;
    };

    socket.on('turn_data',function(data){
      console.log(currentTurn);
      console.log(data);
      Object.assign(currentTurn.roles,data['roles']);
      Object.assign(currentTurn.team,data['team']);
    });

    socket.on('roll_result',function(data){
      console.log("ROLL RESULT RECEIVED: ",data);
      Object.assign(currentTurn.modifier,data);
    });

    return {
      startGame : startGame,
      startTurn : startTurn,
      currentGame : currentGame,
      currentTurn : currentTurn,
      setGame : setGame,
      getGame : getGame
    };

}]);
